import yt_dlp

def get_video_info(video_url):
    ydl_opts = {
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(video_url, download=False)
            return {
                'title': info.get('title', ''),
                'thumbnail': info.get('thumbnail', ''),
            }
        except Exception as e:
            raise Exception(f"Ошибка при получении информации о видео: {str(e)}")

def download_youtube_video(video_url, download_path):
    ydl_opts = {
        'format': 'best',
        'outtmpl': f'{download_path}/%(title)s.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

if __name__ == '__main__':
    video_url = input('Введите ссылку на видео YouTube: ')
    download_youtube_video(video_url)
