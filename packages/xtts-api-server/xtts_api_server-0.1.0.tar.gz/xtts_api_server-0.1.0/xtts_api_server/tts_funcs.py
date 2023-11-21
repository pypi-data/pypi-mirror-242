# tts.py

import torch
from TTS.api import TTS
from loguru import logger
import os

# List of supported language codes
supported_languages = {
    "ar":"Arabic",
    "pt":"Brazilian Portuguese",
    "zh-cn":"Chinese",
    "cs":"Czech",
    "nl":"Dutch",
    "en":"English",
    "fr":"French",
    "de":"German",
    "it":"Italian",
    "pl":"Polish",
    "ru":"Russian",
    "es":"Spanish",
    "tr":"Turkish",
    "ja":"Japanese",
    "ko":"Korean",
    "hu":"Hungarian"
}

reversed_supported_languages = {name: code for code, name in supported_languages.items()}

class TTSWrapper:
    def __init__(self,output_folder = "./output", speaker_folder="./speakers"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        # self.model = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(self.device)
        self.speaker_folder = speaker_folder
        self.output_folder = output_folder

        self.create_directories()
    
    def load_model(self):
        self.model = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(self.device)

    def create_directories(self):
        # A list of all mystical places to be checked or conjured.
        directories = [self.output_folder, self.speaker_folder]

        for sanctuary in directories:
            # Ensure the path is absolute and normalized to prevent any sorcery!
            absolute_path = os.path.abspath(os.path.normpath(sanctuary))

            if not os.path.exists(absolute_path):
                # If it does not exist in this dimension, then we must bring it into being!
                os.makedirs(absolute_path)
                print(f"The sacred space at {absolute_path} has been manifested!")
            else:
                # If it exists already, let us acknowledge its ancient presence.
                print(f"The venerable domain at {absolute_path} stands firm.")

    def set_speaker_folder(self, folder):
        if os.path.exists(folder) and os.path.isdir(folder):
            self.speaker_folder = folder
            self.create_directories()
            logger.info(f"Speaker folder is set to {folder}")
        else:
            raise ValueError("Provided path is not a valid directory")

    def set_out_folder(self, folder):
        if os.path.exists(folder) and os.path.isdir(folder):
            self.output_folder = folder
            self.create_directories()
            logger.info(f"Output folder is set to {folder}")
        else:
            raise ValueError("Provided path is not a valid directory")

    def list_speakers(self):
        speakers_list = [f for f in os.listdir(self.speaker_folder) if f.endswith('.wav')]
        return speakers_list

    def get_speakers(self):
        # Use os.path.splitext to split off the extension and take only the name
        speakers_list = [os.path.splitext(f)[0] for f in os.listdir(self.speaker_folder) if f.endswith('.wav')]
        return speakers_list
    
    def list_languages(self):
        return reversed_supported_languages

    def process_tts_to_file(self, text, speaker_name_or_path, language, file_name_or_path="out.wav"):
        try:
            # Load the model if it's not already loaded
            if not hasattr(self, "model"):
                self.load_model()
            # Check if the speaker path is a .wav file or just the name
            if speaker_name_or_path.endswith('.wav'):
                if os.path.isabs(speaker_name_or_path):
                    # If it's an absolute path for the speaker file
                    speaker_wav = speaker_name_or_path
                else:
                    # It's just a filename; append it to the speakers folder
                    speaker_wav = os.path.join(self.speaker_folder, speaker_name_or_path)
            else:
                # Look for the corresponding .wav in our list of speakers
                speakers_list = self.list_speakers()
                if f"{speaker_name_or_path}.wav" in speakers_list:
                    speaker_wav = os.path.join(self.speaker_folder, f"{speaker_name_or_path}.wav")
                else:
                    raise ValueError(f"Speaker {speaker_name_or_path} not found.")

            # Determine output path based on whether a full path or a file name was provided
            if os.path.isabs(file_name_or_path):
                # An absolute path was provided by user; use as is.
                output_file = file_name_or_path
            else:
                # Only a filename was provided; prepend with output folder.
                output_file = os.path.join(self.output_folder, file_name_or_path)

            self.model.tts_to_file(
                text=text,
                speaker_wav=speaker_wav,
                language=language,
                file_path=output_file  # Assuming tts_to_file takes 'file_path' as an argument.
            )

            return output_file

        except Exception as e:
            raise e  # Propagate exceptions for endpoint handling.



        