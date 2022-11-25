import pandas as pd
import re
import os


class Movie:
    def __init__(self, name):
        self.name = name
        self.getContents()
        self.seperate_scenes()
        self.characters_per_scene()
        
    def getContents(self):
        with open(self.name,'r') as f:
            movie_contents = f.readlines()
        contents = []
        for content in movie_contents:
            content = content.strip('\n').strip()
            if content:
                contents.append(content)
        i = 1
        while i:
            if not contents[i][0].isupper():
                contents[i-1] += ' ' + contents[i]
                del contents[i]
            else:
                i+=1
            if i>=len(contents):
                i = 0
        self.contents = contents
        _, speaker, _ = self.extract_sentence(self.contents)
        self.speaker = set(speaker)
    
    def extract_sentence(self, contents):
        dialog, speaker, contents = self.seperate_dialog(contents)
        new_contents = []
        for content in contents:
            if '.' in content:
                for con in content.split('.'):
                    if con:
                        new_contents.append(con+'.')
            else:
                new_contents.append(content)
        return dialog, speaker, new_contents
    
    def seperate_dialog(self,contents):
        dialog = []
        speaker = []
        nor_sent = []
        stop_words = ['-',":","CONTINUE","END","NEARBY","OUTSIDE"]
        swit = 0
        for i in range(len(contents)):
            if swit:
                swit = 0
                continue
            text = contents[i]
            if any(word in text for word in stop_words):
                continue
            text = re.sub(r'\([^)]*\)', '', text).strip()
            #text = text.replace('.','')
            if text.isupper() and text.count(' ')<2 and i+1!=len(contents) and '!' not in text:
                speaker.append(re.sub('[^a-zA-Z]','',text).replace(' ',''))
                dialog.append(contents[i+1])
                swit = 1
                continue
            nor_sent.append(contents[i])
        return dialog, speaker, nor_sent
    
    def seperate_scenes(self):
        stop_words = ['INT','EXT','DAY','NIGHT','---------------------------']
        scenes =[]
        scene = []
        start = 1
        for cont in self.contents:
            if any(word in cont for word in stop_words):
                if start:
                    start = 0
                    scene = []
                    continue
                if scene:
                    scenes.append(scene)
                scene = []
                continue
            if cont:    
                scene.append(cont)
            
        self.scenes = scenes
        
    def characters_per_scene(self):
        self.scene_dict = {}
        for i, scene in enumerate(self.scenes):
            char_sent = {}
            dialog, speaker, nor_sent = self.extract_sentence(scene)
            for char, dia in zip(speaker, dialog):
                if char not in char_sent.keys():
                    char_sent[char] = [dia]
                else:
                    char_sent[char] += [dia]
            for sent in nor_sent:
                for char in self.speaker:
                    if char.lower()+' ' in sent.lower() or char.lower()+'.' in sent.lower():
                        if char not in char_sent.keys():
                            char_sent[char] = [sent]
                        else:
                            char_sent[char] += [sent]
            self.scene_dict[i+1] = char_sent
    
    def find_maincharacter_name(self):
        num_occur = Counter(self.speaker)
        main_characters_list = num_occur.most_common(5)
        main_characters = []
        for character, count in main_characters_list:
            main_characters.append(character)
        return main_characters

