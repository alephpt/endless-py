import numpy as np
from typing import List, Tuple

class Quaternion:
    """
    A class representing a quaternion.
    """
    def __init__(self, axis: List[float], angle: float) -> None:
        """
        Creates a quaternion from an axis and an angle.

        Parameters:
        axis (List[float]): The axis of rotation.
        angle (float): The angle of rotation in radians.
        """
        self.w = np.cos(angle/2)
        self.x = axis[0] * np.sin(angle/2)
        self.y = axis[1] * np.sin(angle/2)
        self.z = axis[2] * np.sin(angle/2)
        
    def __getitem__(self, b):
        """
        Returns the value of the quaternion at the given index.
        """
        if isinstance(b, int):
            if b == 0:
                return self.x
            elif b == 1:
                return self.y
            elif b == 2:
                return self.z
            elif b == 3:
                return self.w
            else:
                raise IndexError("Quaternion index out of range")
        elif isinstance(b, slice):  
            if b == slice(None):
                return [self.x, self.y, self.z, self.w]
            else:
                [self.x, self.y, self.z, self.w][b.start:b.stop:b.step]
        elif isinstance(b, tuple):
            if len(b) == 2:
                if isinstance(b[0], int) and isinstance(b[1], int):
                    return [self[b[0]], self[b[1]]]
                else:
                    raise IndexError("Quaternion slice must be [:]")
            else:
                raise IndexError("Quaternion slice must be [:]")
        else:
            return self.__dict__[b] if b in self.__dict__ else None
    
    def __repr__(self):
        return f"Quaternion({self.x}, {self.y}, {self.z}, {self.w})"
    
    def __mul__(self, other: 'Quaternion') -> 'Quaternion':
        """
        Multiplies two quaternions.

        Parameters:
        other (Quaternion): The quaternion to multiply by.

        Returns:
        Quaternion: The product of the two quaternions.
        """
        w = self.w*other.w - self.x*other.x - self.y*other.y - self.z*other.z
        x = self.w*other.x + self.x*other.w + self.y*other.z - self.z*other.y
        y = self.w*other.y - self.x*other.z + self.y*other.w + self.z*other.x
        z = self.w*other.z + self.x*other.y - self.y*other.x + self.z*other.w
        return Quaternion([x, y, z], w)
    
    def __add__(self, other: 'Quaternion') -> 'Quaternion':
        """
        Adds two quaternions.

        Parameters:
        other (Quaternion): The quaternion to add.

        Returns:
        Quaternion: The sum of the two quaternions.
        """
        return Quaternion([self.x+other.x, self.y+other.y, self.z+other.z], self.w+other.w)
    
    # += operator
    def __iadd__(self, other: 'Quaternion') -> 'Quaternion':
        """
        Adds a quaternion to the current quaternion.

        Parameters:
        other (Quaternion): The quaternion to add.

        Returns:
        Quaternion: The sum of the two quaternions.
        """
        self.x += other.x
        self.y += other.y
        self.z += other.z
        self.w += other.w
        return self
    
    # divide by scalar
    def __truediv__(self, other: float) -> 'Quaternion':
        """
        Divides a quaternion by a scalar.

        Parameters:
        other (float): The scalar to divide by.

        Returns:
        Quaternion: The quotient of the quaternion and the scalar.
        """
        return Quaternion([self.x/other, self.y/other, self.z/other], self.w/other)
    
    def norm(self) -> float:
        """
        Returns the norm of the quaternion.

        Returns:
        Quaternion: The norm of the quaternion.
        """
        return np.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)
    
    def rotate(self, v: List[float]) -> List[float]:
        """
        Rotates a vector by the quaternion.

        Parameters:
        v (List[float]): The vector to rotate.

        Returns:
        List[float]: The rotated vector.
        """
        qv = np.array([self.x, self.y, self.z])
        uv = np.cross(qv, v)
        uuv = np.cross(qv, uv)
        return v + 2*(self.w*uv + uuv)
    
    @classmethod
    def from_two_vectors(cls, v1: List[float], v2: List[float]) -> 'Quaternion':
        """
        Creates a quaternion from two vectors.
        
        Parameters:
        v1 (List[float]): The first vector.
        v2 (List[float]): The second vector.

        Returns:
        Quaternion: The quaternion representing the rotation from v1 to v2.
        """
        v1 = np.array(v1)
        v2 = np.array(v2)
        v1 /= np.linalg.norm(v1)
        v2 /= np.linalg.norm(v2)
        axis = np.cross(v1, v2)
        angle = np.arccos(np.dot(v1, v2))
        return cls(axis, angle)

    def to_matrix(self) -> np.array:
        """
        Returns the rotation matrix corresponding to the quaternion
        
        Returns:
        np.array: The rotation matrix.
        """
        x, y, z, w = self.x, self.y, self.z, self.w
        matrix = np.array([[1 - 2*y**2 - 2*z**2, 2*x*y - 2*z*w, 2*x*z + 2*y*w],
                        [2*x*y + 2*z*w, 1 - 2*x**2 - 2*z**2, 2*y*z - 2*x*w],
                        [2*x*z - 2*y*w, 2*y*z + 2*x*w, 1 - 2*x**2 - 2*y**2]])
        return matrix
    
    @classmethod
    def from_matrix(cls, matrix) -> 'Quaternion':
        """
        Creates a quaternion from a rotation matrix.
        
        Parameters:
        matrix (np.array): The rotation matrix.

        Returns:
        Quaternion: The quaternion corresponding to the rotation matrix.
        """
        w = np.sqrt(1 + matrix[0, 0] + matrix[1, 1] + matrix[2, 2])/2
        x = (matrix[2, 1] - matrix[1, 2])/(4*w)
        y = (matrix[0, 2] - matrix[2, 0])/(4*w)
        z = (matrix[1, 0] - matrix[0, 1])/(4*w)
        return cls([x, y, z], w)
    
    def to_euler(self) -> List[float]:
        """
        Returns the euler angles corresponding to the quaternion
        
        Returns:
        List[float]: The euler angles.
        """
        x, y, z, w = self.x, self.y, self.z, self.w
        phi = np.arctan2(2*(w*x + y*z), 1 - 2*(x**2 + y**2))
        theta = np.arcsin(2*(w*y - z*x))
        psi = np.arctan2(2*(w*z + x*y), 1 - 2*(y**2 + z**2))
        return [phi, theta, psi]
    
    @classmethod
    def from_euler_angles(cls, phi, theta, psi) -> 'Quaternion':
        """
        Creates a quaternion from euler angles.
        
        Parameters:
        phi (float): The first euler angle.
        theta (float): The second euler angle.
        psi (float): The third euler angle.

        Returns:
        Quaternion: The quaternion corresponding to the euler angles.
        """
        w = np.cos(phi/2)*np.cos(theta/2)*np.cos(psi/2) + np.sin(phi/2)*np.sin(theta/2)*np.sin(psi/2)
        x = np.sin(phi/2)*np.cos(theta/2)*np.cos(psi/2) - np.cos(phi/2)*np.sin(theta/2)*np.sin(psi/2)
        y = np.cos(phi/2)*np.sin(theta/2)*np.cos(psi/2) + np.sin(phi/2)*np.cos(theta/2)*np.sin(psi/2)
        z = np.cos(phi/2)*np.cos(theta/2)*np.sin(psi/2) - np.sin(phi/2)*np.sin(theta/2)*np.cos(psi/2)
        return cls([x, y, z], w)
    
    def to_axis_angle(self) -> Tuple[List[float], float]:
        """
        Returns the axis and angle corresponding to the quaternion
        
        Returns:
        List[float]: The axis and angle.
        """
        angle = 2*np.arccos(self.w)
        axis = [self.x, self.y, self.z]
        return axis, angle
    
    @classmethod
    def from_axis_angle(cls, axis, angle) -> 'Quaternion':
        """
        Creates a quaternion from an axis and angle.
        
        Parameters:
        axis (List[float]): The axis.
        angle (float): The angle.

        Returns:
        Quaternion: The quaternion corresponding to the axis and angle.
        """
        axis = np.array(axis)
        axis = axis / np.linalg.norm(axis)
        w = np.cos(angle/2)
        x = axis[0]*np.sin(angle/2)
        y = axis[1]*np.sin(angle/2)
        z = axis[2]*np.sin(angle/2)
        return cls([x, y, z], w)
    
    def to_rotation_vector(self) -> List[float]:
        """
        Returns the rotation vector corresponding to the quaternion
        
        Returns:
        List[float]: The rotation vector.
        """
        angle, axis = self.to_axis_angle()
        return angle*axis
    
    @classmethod
    def from_rotation_vector(cls, rotation_vector) -> 'Quaternion':
        """
        Creates a quaternion from a rotation vector.
        
        Parameters:
        rotation_vector (List[float]): The rotation vector.

        Returns:
        Quaternion: The quaternion corresponding to the rotation vector.
        """
        angle = np.linalg.norm(rotation_vector)
        axis = rotation_vector/angle
        return cls.from_axis_angle(axis, angle)
    
    def to_unit_vector(self) -> List[float]:
        """
        Returns the unit vector corresponding to the quaternion
        
        Returns:
        List[float]: The unit vector.
        """
        return [self.x, self.y, self.z]

    def to_unit_quaternion(self) -> 'Quaternion':
        """
        Returns the unit quaternion corresponding to the quaternion
        
        Returns:
        Quaternion: The unit quaternion.
        """
        return self/self.norm()

    def to_rotation_matrix(self) -> np.array:
        """
        Returns the rotation matrix corresponding to the quaternion as a 64-byte np.array
        
        Returns:
        64-byte np.array: The rotation matrix.
        """
        return self.to_matrix().astype(np.float64)
    
    def conjugate(self) -> 'Quaternion':
        """
        Returns the conjugate of the quaternion
        
        Returns:
        Quaternion: The conjugate.
        """
        return Quaternion([-self.x, -self.y, -self.z], self.w)
    
    def inverse(self) -> 'Quaternion':
        """
        Returns the inverse of the quaternion
        
        Returns:
        Quaternion: The inverse.
        """
        return self.conjugate()/self.norm()**2
    
    def to_np_array(self) -> np.array:
        """
        Returns the quaternion as a 64-byte np.array
        
        Returns:
        64-byte np.array: The quaternion.
        """
        return np.array([self.x, self.y, self.z], dtype=np.float64)
    
    def normalized_np_array(self) -> np.array:
        """
        Returns the normalized quaternion as a 64-byte np.array
        
        Returns:
        64-byte np.array: The normalized quaternion.
        """
        return self.to_np_array()/self.norm()