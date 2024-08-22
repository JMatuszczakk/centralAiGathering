import json
import random
#read the json file
with open('accessories.json') as f:
    all_accessories = json.load(f)

#generate the prompt
def generatePrompt():
    #get 3 random accessories
    accessories = random.sample(all_accessories, 3)
    
    prompt = (f"A cryptopunk pixelart nft of a tiger that has {', '.join(accessories)}. "
                    f"Style is pixelart cryptopunk, so only the upper part of their body is visible, "
                    f"it has a tiger pattern, and it has a punk style. The background is homogeneous. The portrait is visible to the bottom of the image. "
                    f"The tiger is looking at the viewer with a fierce expression. The image is like a portrait to the bottom of the artpiece, not an icon. It is not a bust. "
                    f"The tiger is facing directly towards the viewer in a frontal pose. Its head is held high, giving an impression of confidence or coolness. The shoulders are visible, suggesting an upright, almost human-like posture. "
                    f"It has a {', '.join(accessories)}."
                    )
    return prompt
if __name__ == "__main__":
    print(generatePrompt())