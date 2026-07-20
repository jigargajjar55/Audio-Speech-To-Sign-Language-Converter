import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from django.contrib.staticfiles import finders
from django.conf import settings
import logging
import os
import uuid
try:
    from moviepy.editor import VideoFileClip, concatenate_videoclips
except ImportError:
    pass

logger = logging.getLogger(__name__)

class NLPService:
    """
    Service class to handle Natural Language Processing tasks.
    It takes an input sentence, tokenizes it, removes stop words,
    determines the tense, lemmatizes words, and maps them to available video assets.
    """
    
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set([
            "mightn't", 're', 'wasn', 'wouldn', 'be', 'has', 'that', 'does', 'shouldn', 'do', 
            "you've",'off', 'for', "didn't", 'm', 'ain', 'haven', "weren't", 'are', "she's", 
            "wasn't", 'its', "haven't", "wouldn't", 'don', 'weren', 's', "you'd", "don't", 
            'doesn', "hadn't", 'is', 'was', "that'll", "should've", 'a', 'then', 'the', 
            'mustn', 'i', 'nor', 'as', "it's", "needn't", 'd', 'am', 'have',  'hasn', 'o', 
            "aren't", "you'll", "couldn't", "you're", "mustn't", 'didn', "doesn't", 'll', 
            'an', 'hadn', 'whom', 'y', "hasn't", 'itself', 'couldn', 'needn', "shan't", 
            'isn', 'been', 'such', 'shan', "shouldn't", 'aren', 'being', 'were', 'did', 
            'ma', 't', 'having', 'mightn', 've', "isn't", "won't"
        ])

    def get_tense(self, tagged_words):
        """Determine the tense of the sentence based on POS tags."""
        tense = {
            "future": len([word for word in tagged_words if word[1] == "MD"]),
            "present": len([word for word in tagged_words if word[1] in ["VBP", "VBZ", "VBG"]]),
            "past": len([word for word in tagged_words if word[1] in ["VBD", "VBN"]]),
            "present_continuous": len([word for word in tagged_words if word[1] in ["VBG"]])
        }
        return tense

    def lemmatize_word(self, word, pos_tag):
        """Lemmatize a single word based on its POS tag."""
        if pos_tag in ['VBG', 'VBD', 'VBZ', 'VBN', 'NN']:
            return self.lemmatizer.lemmatize(word, pos='v')
        elif pos_tag in ['JJ', 'JJR', 'JJS', 'RBR', 'RBS']:
            return self.lemmatizer.lemmatize(word, pos='a')
        else:
            return self.lemmatizer.lemmatize(word)

    def process_text(self, text):
        """
        Main processing function.
        Returns a list of words or characters that correspond to available video assets.
        """
        if not text:
            return []
            
        try:

        # Tokenize the sentence
            words = word_tokenize(text.lower())
            tagged = nltk.pos_tag(words)
            
            tense = self.get_tense(tagged)
            
            # Remove stopwords and apply lemmatization
            filtered_text = []
            for w, p in zip(words, tagged):
                if w not in self.stop_words:
                    lemmatized_word = self.lemmatize_word(w, p[1])
                    filtered_text.append(lemmatized_word)

            # Basic pronoun swap and capitalization matching
            temp = []
            for w in filtered_text:
                if w.lower() == 'i':
                    temp.append('Me')
                else:
                    temp.append(w.capitalize())

            words = temp
            
            # Tense adjustment keywords
            if tense:
                probable_tense = max(tense, key=tense.get)
                if probable_tense == "past" and tense["past"] >= 1:
                    words = ["Before"] + words
                elif probable_tense == "future" and tense["future"] >= 1:
                    if "Will" not in words:
                        words = ["Will"] + words
                elif probable_tense == "present":
                    if tense["present_continuous"] >= 1:
                        words = ["Now"] + words

            # Map to available videos or break down into characters
            final_animation_sequence = []
            for w in words:
                path = "videos/" + w + ".mp4"
                f = finders.find(path)
                
                # Splitting the word into characters if its animation is not present in database
                if not f:
                    for c in w:
                        final_animation_sequence.append(c.capitalize())
                else:
                    final_animation_sequence.append(w)

            return final_animation_sequence
            
        except Exception as e:
            logger.error(f"NLP Processing Error for text '{text}': {str(e)}")
            return []

    def stitch_video(self, words):
        """
        Takes a list of words, finds their videos, and stitches them into a single video.
        Returns the relative URL to the stitched video.
        """
        if not words:
            return None
            
        video_clips = []
        for w in words:
            path = finders.find("videos/" + w + ".mp4")
            if path:
                try:
                    clip = VideoFileClip(path)
                    video_clips.append(clip)
                except Exception as e:
                    logger.error(f"Error loading clip {path}: {str(e)}")
                    
        if not video_clips:
            return None
            
        try:
            final_clip = concatenate_videoclips(video_clips, method="compose")
            
            filename = f"stitched_{uuid.uuid4().hex}.mp4"
            output_dir = os.path.join(settings.BASE_DIR, "assets", "videos", "cache")
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                
            output_path = os.path.join(output_dir, filename)
            
            # Write the stitched video, forcing yuv420p pixel format for browser compatibility
            final_clip.write_videofile(
                output_path,
                codec="libx264",
                audio_codec="aac",
                preset="ultrafast",
                logger=None,
                ffmpeg_params=["-pix_fmt", "yuv420p"]
            )
            
            # Close clips to free memory
            for clip in video_clips:
                clip.close()
            final_clip.close()
            
            return f"/static/videos/cache/{filename}"
        except Exception as e:
            logger.error(f"Error stitching video: {str(e)}")
            return None
