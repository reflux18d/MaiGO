from pydub import AudioSegment
aac_file_path="D:/程序设计实习/MaiGO/try.aac"
def convert_aac_to_wav(aac_file_path):
    aac_audio = AudioSegment.from_file(aac_file_path, format='aac')
    aac_audio.export('output.wav', format='wav')

# 调用函数，将实际的AAC文件路径传入
convert_aac_to_wav(aac_file_path) 