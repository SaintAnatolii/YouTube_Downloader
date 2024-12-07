import flet as ft
from you_tube_downloader import download_youtube_video, get_video_info
import os
import requests
from io import BytesIO

def main(page: ft.Page):
    # Configure the page
    page.title = "YouTube Video Downloader"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 50
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # Create UI elements
    title = ft.Text(
        "YouTube Video Downloader",
        size=32,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )
    
    url_input = ft.TextField(
        label="Введите ссылку на видео YouTube",
        width=600,
        text_align=ft.TextAlign.LEFT,
        border_radius=10,
    )

    video_info_container = ft.Container(
        content=ft.Column(
            controls=[],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        visible=False
    )

    video_title = ft.Text(
        size=18,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )

    video_thumbnail = ft.Image(
        width=320,
        height=180,
        fit=ft.ImageFit.CONTAIN,
        visible=False
    )

    video_info_container.content.controls.extend([
        video_title,
        video_thumbnail
    ])

    path_text = ft.Text(
        "Выберите папку для сохранения:",
        size=16,
        color=ft.colors.GREY_700,
    )
    
    download_path = ft.Text(
        os.path.expanduser("~/Downloads"),
        size=14,
        color=ft.colors.BLUE_600,
        width=400,
        text_align=ft.TextAlign.LEFT,
    )
    
    status_text = ft.Text(
        size=16,
        color=ft.colors.GREY_700,
    )
    
    progress_ring = ft.ProgressRing(visible=False)

    def get_directory_result(e: ft.FilePickerResultEvent):
        if e.path:
            download_path.value = e.path
            page.update()

    directory_picker = ft.FilePicker(
        on_result=get_directory_result
    )

    page.overlay.append(directory_picker)

    def pick_directory(e):
        directory_picker.get_directory_path()

    pick_folder_btn = ft.ElevatedButton(
        "Выбрать папку",
        icon=ft.icons.FOLDER_OPEN,
        on_click=pick_directory,
    )

    def on_url_change(e):
        if url_input.value:
            try:
                # Show loading state
                status_text.value = "Получение информации о видео..."
                status_text.color = ft.colors.BLUE_600
                video_info_container.visible = False
                page.update()

                # Get video info
                info = get_video_info(url_input.value)
                
                # Update UI with video info
                video_title.value = info['title']
                
                # Load and display thumbnail
                video_thumbnail.src = info['thumbnail']
                video_thumbnail.visible = True
                
                # Show video info container
                video_info_container.visible = True
                status_text.value = ""
                page.update()
                
            except Exception as e:
                status_text.value = str(e)
                status_text.color = ft.colors.RED_600
                video_info_container.visible = False
                page.update()

    url_input.on_change = on_url_change

    def download_clicked(e):
        if not url_input.value:
            status_text.value = "Пожалуйста, введите ссылку на видео"
            status_text.color = ft.colors.RED_600
            page.update()
            return
        
        if not download_path.value:
            status_text.value = "Пожалуйста, выберите папку для сохранения"
            status_text.color = ft.colors.RED_600
            page.update()
            return
        
        # Show loading state
        download_btn.disabled = True
        progress_ring.visible = True
        status_text.value = "Загрузка видео..."
        status_text.color = ft.colors.BLUE_600
        page.update()
        
        try:
            # Download the video
            download_youtube_video(url_input.value, download_path.value)
            
            # Show success message
            status_text.value = "Видео успешно загружено!"
            status_text.color = ft.colors.GREEN_600
            
        except Exception as e:
            # Show error message
            status_text.value = f"Ошибка: {str(e)}"
            status_text.color = ft.colors.RED_600
            
        finally:
            # Reset UI state
            download_btn.disabled = False
            progress_ring.visible = False
            page.update()
    
    download_btn = ft.ElevatedButton(
        "Скачать",
        width=200,
        height=50,
        style=ft.ButtonStyle(
            color={
                ft.MaterialState.DEFAULT: ft.colors.WHITE,
                ft.MaterialState.DISABLED: ft.colors.GREY_400,
            },
            bgcolor={
                ft.MaterialState.DEFAULT: ft.colors.BLUE_600,
                ft.MaterialState.DISABLED: ft.colors.GREY_300,
            },
            padding=15,
        ),
        on_click=download_clicked,
    )

    # Create layout
    page.add(
        ft.Column(
            [
                title,
                ft.Container(height=40),
                url_input,
                ft.Container(height=20),
                video_info_container,
                ft.Container(height=20),
                path_text,
                ft.Row(
                    [download_path, pick_folder_btn],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Container(height=20),
                ft.Row(
                    [download_btn, progress_ring],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Container(height=20),
                status_text,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
