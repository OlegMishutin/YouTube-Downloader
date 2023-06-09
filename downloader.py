import os
from pytube import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip


class Downloader():
    def __init__(self):
        self.__video=None
        self.__cacheFiles=["videoCache.mp4", "audioCache.mp3"]
        self.__codecs={"2160p": [266, 305, 313, 315, 337, 401, 701],
                       "1440p": [264, 271, 308, 336, 304, 400, 700],
                       "1080p": [137, 248, 299, 303, 335, 399, 699],
                       "720p": [136, 247, 298, 302, 334, 398, 698],
                       "480p": [135, 244, 333, 397, 697],
                       "360p": [134, 243, 332, 396, 696],
                       "240p": [133, 242, 331, 395, 695],
                       "144p": [160, 278, 330, 394, 694]}

    def GetVideoInfo(self, source: str) -> str:
        try:
            self.__video=YouTube(source, use_oauth=True, allow_oauth_cache=True)

            return f"Author: {self.__video.author}; Title: {self.__video.title}"
        except Exception:
            self.__video=None

            return "Incorrect link or server error" if source else ""

    def GetVideoItag(self, resolution: str):
        return self.__video.streams.filter(progressive=False, res=resolution).itag_index.keys()

    def GetVideoResolutions(self) -> list:
        availableRes=[]

        if self.__video:
            for resolution in self.__codecs:
                for codec in self.__codecs.get(resolution):
                    if codec in self.GetVideoItag(resolution):
                        availableRes.append(resolution)
                        break

        return availableRes

    def GetVideoCodec(self, resolution) -> list:
        return list(self.GetVideoItag(resolution))[0]

    def CombineAudioVideoFiles(self, pathToCombine: str):
        videoClip, audioClip=VideoFileClip(self.__cacheFiles[0]), AudioFileClip(self.__cacheFiles[1])

        videoClip.audio=CompositeAudioClip([audioClip])
        videoClip.write_videofile(f"{pathToCombine}/{self.__video.title}.mp4", temp_audiofile="tempAudioFile.mp3")

    def DownloadVideo(self, source: str, pathForSaving: str, resolution: str) -> str:
        if self.__video:
            try:
                mp4Downloader=self.__video.streams.get_by_itag(self.GetVideoCodec(resolution))
                mp4Downloader.download(filename=self.__cacheFiles[0])

                mp3Downloader=self.__video.streams.get_by_itag(251)
                mp3Downloader.download(filename=self.__cacheFiles[1])

                self.CombineAudioVideoFiles(pathForSaving)
            except Exception:
                return "Server error, try again"
            finally:
                for cacheFile in self.__cacheFiles:
                    os.remove(f"{os.getcwd()}/{cacheFile}")

            return f"Video downloaded in {pathForSaving}"
        return "Incorrect link or server error"