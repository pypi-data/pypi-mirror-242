from ..base import Async, ProtoHttp, ProtoPath, T, BaseClient


class AsyncClient(BaseClient[Async]):
    async def __call__(self, path: ProtoPath[T], **kwargs) -> T:
        request = self._build_request(path, **kwargs)
        response = await self.http.fetch(request)
        self._check_response(response)
        return self._build_result(response, path)

    @staticmethod
    def default_http() -> ProtoHttp[Async]:
        from .http.httpx_ import AsyncHttpxSession

        return AsyncHttpxSession()
