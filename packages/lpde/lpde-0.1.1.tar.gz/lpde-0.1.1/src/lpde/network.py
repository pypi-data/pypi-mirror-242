"""
Copyright © 2022 Felix P. Kemeth

Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the “Software”), to deal in the Software without
restriction, including without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from configparser import SectionProxy

import findiff
import numpy as np
import torch


class _BaseNetwork(torch.nn.Module):
    """
    Pytorch PDE neural network.

    Args:
        config: Config with hyperparameters
        n_vars: Number of system variables
    """

    def __init__(self, config: SectionProxy, n_vars: int):
        super().__init__()
        self.kernel_size = config.getint('kernel_size')
        self.n_derivs = config.getint('n_derivs')
        self.device = config['device']
        self.use_param = config.getboolean('use_param')
        self.n_vars = n_vars

        self.register_buffer(
            'coeffs', self.get_coeffs(max_deriv=self.n_derivs))

        self.network = self.get_network(config)
        self.trainable_parameters = sum(p.numel()
                                        for p in self.network.parameters() if p.requires_grad)

    def get_off_set(self) -> int:
        """
        Get width of boundaries.

        Returns:
            Width of boundary
        """
        return int((self.kernel_size-1)/2)


class Network1D(_BaseNetwork):
    """
    Pytorch 1-D PDE neural network.

    Args:
        config: Config with hyperparameters
        n_vars: Number of system variables
    """

    def get_network(self, config: SectionProxy) -> torch.nn.Module:
        """
        Create network stack of PDE model.
        """
        layers = []
        if self.use_param:
            num_features = int(self.n_vars*(self.n_derivs+1) +
                               int(config.getint('num_params')))
        else:
            num_features = int(self.n_vars*(self.n_derivs+1))

        n_channels = config.getint('n_filters')

        for _ in range(config.getint('n_layers')):
            layers.append(torch.nn.Conv1d(
                num_features, n_channels, (1), stride=1, padding=0, bias=True))
            layers.append(torch.nn.SiLU())
            num_features = n_channels

        # Output layer
        layers.append(torch.nn.Conv1d(
            num_features, self.n_vars, (1), stride=1, padding=0, bias=True))

        return torch.nn.Sequential(*layers)

    def get_coeffs(self, min_deriv: int = 0, max_deriv: int = 5) -> torch.Tensor:
        """
        Get finite difference coefficients.

        Args:
            min_deriv: Order of minimal derivative
            max_deriv: Order of maximal derivative

        Returns:
            Tensor with finite difference coefficients
        """
        assert max_deriv > min_deriv, 'Max derivative should be larger than min derivative.'
        assert min_deriv >= 0, 'Min derivative should be positive.'
        assert max_deriv < self.kernel_size, 'Max derivative should not be larger than kernel size.'

        coeffs = np.zeros((max_deriv-min_deriv+1, 1, self.kernel_size))
        # Finite difference coefficients
        for i in range(min_deriv, max_deriv+1):
            # Get coefficient for certain derivative with maximal acc order for given kernel_size
            fd_coeff = np.array([1.])
            if i > 0:
                acc_order = 0
                while len(fd_coeff) < self.kernel_size:
                    acc_order += 2
                    fd_coeff = findiff.coefficients(
                        i, acc_order)['center']['coefficients']
                assert len(fd_coeff) == self.kernel_size, \
                    'Finite difference coefficients do not match kernel'
                coeffs[i, 0, :] = fd_coeff
            else:
                coeffs[i, 0, int((self.kernel_size-1)/2)] = 1.0
        return torch.tensor(coeffs, requires_grad=False,
                            dtype=torch.get_default_dtype()).to(self.device)

    def calc_derivs(self, input_tensor: torch.Tensor, delta_x: torch.Tensor) -> torch.Tensor:
        """
        Calculate derivativers of input snapshot.

        Args:
            input_tensor: Tensor with input features
            delta_x: Tensor with spatial resolution
            param: Tensor with system parameters

        Returns:
            Spatial derivative tensor
        """
        finite_diffs = torch.cat([
            torch.nn.functional.conv1d(
                input_tensor[:, i].unsqueeze(1),
                self.coeffs) for i in range(input_tensor.shape[1])
        ], dim=1)
        scales = torch.cat([torch.pow(delta_x.unsqueeze(1), i)
                            for i in range(self.coeffs.shape[0])], axis=-1)
        scales = scales.repeat(1, self.n_vars)
        scales = scales.unsqueeze(2).repeat(
            1, 1, finite_diffs.shape[-1]).to(self.device)
        return finite_diffs/scales

    def forward(self,
                input_tensor: torch.Tensor,
                delta_x: torch.Tensor,
                param: torch.Tensor = torch.empty(1)) -> torch.Tensor:
        """
        Forward pass through PDE neural network.

        Args:
            input_tensor: Tensor with input features
            delta_x: Tensor with spatial resolution
            param: Tensor with system parameters

        Returns:
            Output prediction tensor
        """
        # Calculate derivatives
        input_tensor = self.calc_derivs(input_tensor, delta_x)
        if self.use_param:
            param = param.unsqueeze(-1).repeat(1, 1, input_tensor.shape[-1])
            input_tensor = torch.cat([input_tensor, param], axis=1)
        # Forward through distributed parameter stack
        input_tensor = self.network(input_tensor)
        return input_tensor


class Network(Network1D):
    """
    Pytorch 1-D PDE neural network.

    Args:
        config: Config with hyperparameters
        n_vars: Number of system variables
    """


class Network2D(_BaseNetwork):
    """
    Pytorch 2-D PDE neural network.

    Args:
        config: Config with hyperparameters
        n_vars: Number of system variables
    """

    def get_network(self, config: SectionProxy) -> torch.nn.Module:
        """
        Create network stack of PDE model.
        """
        layers = []
        if self.use_param:
            num_features = int(2*self.n_vars*(self.n_derivs+1) +
                               int(config.getint('num_params')))
        else:
            num_features = int(2*self.n_vars*(self.n_derivs+1))

        n_channels = config.getint('n_filters')

        for _ in range(config.getint('n_layers')):
            layers.append(torch.nn.Conv2d(
                num_features, n_channels, (1), stride=1, padding=0, bias=True))
            layers.append(torch.nn.SiLU())
            num_features = n_channels

        # Output layer
        layers.append(torch.nn.Conv2d(
            num_features, self.n_vars, (1), stride=1, padding=0, bias=True))

        return torch.nn.Sequential(*layers)

    def get_coeffs(self, min_deriv: int = 0, max_deriv: int = 5) -> torch.Tensor:
        """
        Get finite difference coefficients.

        Args:
            min_deriv: Order of minimal derivative
            max_deriv: Order of maximal derivative

        Returns:
            Tensor with finite difference coefficients
        """
        assert max_deriv > min_deriv, 'Max derivative should be larger than min derivative.'
        assert min_deriv >= 0, 'Min derivative should be positive.'
        assert max_deriv < self.kernel_size, 'Max derivative should not be larger than kernel size.'

        coeffs = np.zeros((2*(max_deriv-min_deriv+1), 1,
                          self.kernel_size, self.kernel_size))
        # Finite difference coefficients
        for i in range(min_deriv, max_deriv+1):
            # Get coefficient for certain derivative with maximal acc order for given kernel_size
            fd_coeff = np.array([1.])
            if i > 0:
                acc_order = 0
                while len(fd_coeff) < self.kernel_size:
                    acc_order += 2
                    fd_coeff = findiff.coefficients(
                        i, acc_order)['center']['coefficients']
                assert len(fd_coeff) == self.kernel_size, \
                    'Finite difference coefficients do not match kernel'
                coeffs[2*i, 0, :, int((self.kernel_size-1)/2)
                       ] = fd_coeff  # x direction
                coeffs[2*i+1, 0, int((self.kernel_size-1)/2),
                       :] = fd_coeff  # y direction
            else:
                coeffs[i, 0, int((self.kernel_size-1)/2),
                       int((self.kernel_size-1)/2)] = 1.0
        return torch.tensor(coeffs, requires_grad=False,
                            dtype=torch.get_default_dtype()).to(self.device)

    def calc_derivs(self,
                    input_tensor: torch.Tensor,
                    delta_x: torch.Tensor,
                    delta_y: torch.Tensor) -> torch.Tensor:
        """
        Calculate derivativers of input snapshot.

        Args:
            input_tensor: Tensor with input features
            delta_x: Tensor with spatial resolution in the x direction
            delta_y: Tensor with spatial resolution in the y direction
            param: Tensor with system parameters

        Returns:
            Spatial derivative tensor
        """
        finite_diffs = torch.cat([
            torch.nn.functional.conv2d(
                input_tensor[:, i].unsqueeze(1),
                self.coeffs) for i in range(input_tensor.shape[1])
        ], dim=1)
        x_scales = torch.cat([torch.pow(delta_x, i)
                              for i in range(int(self.coeffs.shape[0]/2))], axis=-1)
        y_scales = torch.cat([torch.pow(delta_y, i)
                              for i in range(int(self.coeffs.shape[0]/2))], axis=-1)
        x_scales = torch.cat(
            (x_scales, x_scales), axis=1).unsqueeze(2).unsqueeze(2).repeat(
                1, 1, finite_diffs.shape[-2], finite_diffs.shape[-1]).to(self.device)
        y_scales = torch.cat(
            (y_scales, y_scales), axis=1).unsqueeze(2).unsqueeze(2).repeat(
                1, 1, finite_diffs.shape[-2], finite_diffs.shape[-1]).to(self.device)
        return torch.cat([finite_diffs[:, ::2]/x_scales, finite_diffs[:, 1::2]/y_scales], axis=1)

    def forward(self,
                input_tensor: torch.Tensor,
                delta_xy: torch.Tensor,
                param: torch.Tensor = torch.empty(1)) -> torch.Tensor:
        """
        Forward pass through PDE neural network.

        Args:
            input_tensor: Tensor with input features
            delta_x: Tensor with spatial resolution in the x direction
            param: Tensor with system parameters

        Returns:
            Output prediction tensor
        """
        # Calculate derivatives
        delta_x, delta_y = torch.split(delta_xy, 1, 1)
        input_tensor = self.calc_derivs(input_tensor, delta_x, delta_y)
        if self.use_param:
            param = param.unsqueeze(-1).repeat(1, 1,
                                               input_tensor.shape[-2], input_tensor.shape[-1])
            input_tensor = torch.cat([input_tensor, param], axis=1)
        # Forward through distributed parameter stack
        input_tensor = self.network(input_tensor)
        return input_tensor
