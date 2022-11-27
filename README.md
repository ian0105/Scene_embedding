# Learning Scene Representation Using a Graph for Understanding Narrative

Members: EunChong Kim, Yun-Gyung Cheong Department of Artificial Intelligence, Sungkyunkwan University, South Korea


## Task Abstraction:
Main task is Movie analysis using scene units.
Convert Scenes of movie script into scene embedding.

## Paper Abstraction:
Studies to analize movie script computationally have existed over the past few years. However, there was no attempt to intensively analyze the scene constituting the script. Scene is an essential foundation for building a film. So we're going to focus on the scene. This paper aims to contstruct scene embedding based on character information. We first divided the script into scene units, and then extracted the character-related information from them. Based on the information, the graph is constructed and learned to create representation of the scene. Using this embedding, we created classification task to verify whether scene embedding reflects the context of the scene. In addition, using the nearest neighbor method, we checked whether embeddings with similar contexts were gathered. Finally, using qualitative evaluation, individual movies were selected to check whether scene embedding was certainly learned according to the context. Through these experiments, we found that scene embedding fully reflects the content of the scene, contains contextual flow, and character-based information was well learned.

## Our model
![image](https://user-images.githubusercontent.com/61653249/204125076-db91153c-6ea8-4cf9-9348-bb393eb21aae.png)
