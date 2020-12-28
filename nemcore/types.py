from collections import UserDict


class BaseResponse(UserDict):
    def __getattr__(self, item):
        if item in self.data:
            return self.data[item]
        raise AttributeError(f'{self} has no attribute {item}')

    def __setattr__(self, key, value):
        raise AttributeError('All response class was readonly.')


class GetUserPlaylistResponse(BaseResponse):
    code: int
