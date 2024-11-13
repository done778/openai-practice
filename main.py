from openai import OpenAI
import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np
import time
client = OpenAI()

def record_audio(duration=5, sample_rate=44100, file_name='recorded_audio.wav'):
    """
    음성을 녹음하고 WAV 파일로 저장하는 함수
    duration: 녹음 시간 (초)
    sample_rate: 샘플링 레이트 (Hz)
    """
    try:
        # 녹음 시작 전 카운트다운
        print("녹음을 준비합니다...")
        for i in range(3, 0, -1):
            print(f"{i}...")
            time.sleep(1)

        print("녹음을 시작합니다!")

        # 음성 녹음
        recording = sd.rec(int(duration * sample_rate),
                         samplerate=sample_rate,
                         channels=1,
                         dtype=np.int16)

        # 녹음이 끝날 때까지 대기
        sd.wait()

        # WAV 파일로 저장
        wav.write(file_name, sample_rate, recording)
        print(f"녹음이 완료되었습니다! {file_name} 파일이 생성되었습니다.")
        return file_name

    except Exception as e:
        print(f"녹음 중 오류가 발생했습니다: {str(e)}")
        return False

def speech_to_text(file_name):
  audio_file= open(file_name, "rb")
  transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file,
    language="en"
  )
  print(transcription.text)

  return transcription.text


def chatgpt(question):
  completion = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
          {"role": "system", "content": "You are an experienced English tutor who graduated from Harvard University in Boston.\
            You are talking to a student who wants to practice speaking English.\
            Help them practice speaking English by talking to your student and\
            While talking to your student, help your student how to say what they would like to say."},
          {
              "role": "user",
              "content": question
          }
      ]
  )

  return completion.choices[0].message.content

def main():
  print("여기는 main 함수입니다.")
  # 음성 녹음
  my_speech = record_audio()
  # 녹음에 성공했다면 녹음한 파일을 텍스트로 변환
  if (my_speech):
    trans_text = speech_to_text(my_speech)
    # 변환된 텍스트를 chatGPT에게 전달
    respawn = chatgpt(trans_text)
    # chatGPT의 답변 출력
    print(respawn)


if __name__ == "__main__":
  main()
