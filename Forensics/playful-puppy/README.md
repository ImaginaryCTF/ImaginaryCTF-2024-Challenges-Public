# playful-puppy
**Category:** Forensics
**Difficulty:** Easy
**Author:** cleverbear57

## Description

I lost my dog in Minecraft. Can you find him? The name of the dog wrapped in "ictf{}" is the flag.

## Distribution

- `playful-puppy.zip`
- `image.png`

## Solution

- Use NBTExplorer to view the entities in the world. Then, you can use google to find that the name of the tag determining collar color is called CollarColor. With further research, you can find that the id of the color "Blue" is 11. Then, use control-F to search for the tag, "CollarColor", with value 11. After a few searches, you can find a dog whose CollarColor is 11, and is of the black variant. The name of the dog will be shown in the data, giving you the flag
