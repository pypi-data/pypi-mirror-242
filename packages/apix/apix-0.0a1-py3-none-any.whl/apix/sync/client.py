from ..base import Sync, ProtoHttp, ProtoPath, T, BaseClient



class SyncClient(BaseClient[Sync]):
    def __call__(self, path: ProtoPath[T], **kwargs) -> T:
        request = self._build_request(path, **kwargs)
        response = self.http.fetch(request)
        self._check_response(response)
        return self._build_result(response, path)

    @staticmethod
    def default_http() -> ProtoHttp[Sync]:
        from .http.httpx_ import SyncHttpxSession

        return SyncHttpxSession()
