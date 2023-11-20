from scan.downloade.downloader import Downloader


class Crawl:
    def __init__(self):
        self.downloader = Downloader()

    async def fetch(self,  url, params=None, data=None, files=None, json=None, content=None,headers=None, cookies=None,
                    verify=True, http2=False, auth=None, proxies=None, allow_redirects=True, stream=False, session=True,
                    timeout=30, cycle=3, tls=False):
        res = await self.downloader.request(
            url, params=params, data=data, files=files, json=json, content=content, headers=headers, proxies=proxies,
            verify=verify, http2=http2, cookies=cookies, auth=auth, allow_redirects=allow_redirects, timeout=timeout,
            cycle=cycle, stream=stream, tls=tls, session=session
        )
        return res

    async def close(self):
        await self.downloader.close()


crawl = Crawl()
__all__ = crawl
