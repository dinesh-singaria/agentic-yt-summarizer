from caption_generator import caption_keyframes

keyframes = [
    "keyframes/scene_1.jpg",
    "keyframes/scene_2.jpg",
    "keyframes/scene_3.jpg"
]

captions = caption_keyframes(keyframes)

print("\n📜 Generated Captions:")
for name, text in captions.items():
    print(f"{name}: {text}")