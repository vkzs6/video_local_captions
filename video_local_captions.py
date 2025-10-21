import os
import whisper
import ffmpeg
from datetime import timedelta

def create_subs(file_name, transcription):
    with open(f'{file_name}.srt', 'w', encoding='utf-8') as srtFile:
        for segment in transcription['segments']:
            startTime = f"0{timedelta(seconds=int(segment['start']))},000"
            endTime = f"0{timedelta(seconds=int(segment['end']))},000"
            text = segment['text']
            segmentId = segment['id'] + 1
            segment_str = f"{segmentId}\n{startTime} --> {endTime}\n{text}\n\n"
            srtFile.write(segment_str)

def add_subtitles(video_file):
    srt_file = f'{os.path.splitext(video_file)[0]}.srt'
    video = ffmpeg.input(video_file)
    audio = video.audio
    # Nome do arquivo de saída
    out_file = f'subtitled_{os.path.basename(video_file)}'
    (
        ffmpeg
        .concat(
            video.filter("subtitles", srt_file),
            audio,
            v=1,
            a=1
        )
        .output(out_file)
        .run()
    )
    print(f"Arquivo final criado: {out_file}")


def transcribe_video(video_file):
    print(f"Processando vídeo: {video_file}")
    model = whisper.load_model("small")
    transcription = model.transcribe(video_file)
    print("Transcrição concluída")
    return transcription


def process_folder(folder):
    for filename in os.listdir(folder):
        if filename.lower().endswith(".mp4"):
            filepath = os.path.join(folder, filename)
            transcription = transcribe_video(filepath)
            base_name = os.path.splitext(filepath)[0]
            create_subs(base_name, transcription)
            add_subtitles(filepath)


if __name__ == "__main__":
    video_folder = "."  # Pasta onde estão os vídeos para processar
    process_folder(video_folder)
