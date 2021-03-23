#! usr/bin/env python
import pygame
import os
import sys
import argparse
import random

def list_pictures(directory):
    picturePaths = []
    for filename in os.listdir(directory):
        if filename[-3:] in ('png', 'gif', 'jpg'):
            picturePaths.append(filename)
    return picturePaths

# Find the average color using mode average (most common)
def find_color_value(picture):
    colors = {}
    for x in range(0, picture.get_width()):
        for y in range(0, picture.get_height()):
            # below, get_at returns a Pygame Color object, which is not 
            # hashable, so we make a RBG tuple of it.
            color = tuple(picture.get_at((x, y)))
            color = (color[0], color[1], color[2])
            try:
                colors[color] += 1
            except:
                colors[color] = 1
    colorsMode = sorted(colors.itervalues(), reverse=True)[0]
    # python complains if colorValue is not initialized
    # outside the for loop, so we reference it here too.
    colorValue = (0, 0, 0)
    for key in sorted(colors.iterkeys(), reverse=True):
        if colors[key] == colorsMode:
            colorValue = key
    return colorValue

# This function assumes the path given is an absolute path.
# Also, depending on the accuracy it may return the same picture
# for different color values.
def scan_pictures(color, directory, accuracy):
    picturePaths = []
    for picPath in list_pictures(directory):
        pictureSurface = pygame.load.image(pic)
        pictureValue = find_color_value(pictureSurface)
        picturePaths.append(picPath)
    # don't use the same pic all the time!
    selectedPath = random.choice(picturePaths)
    picture = pygame.image.load(selectedPath)
    return picture

def generate_mosaic(picture, tileSize, directory, accuracy):
    pWidth = picture.get_width()
    pHeight = picture.get_height()
    mosaic = pygame.Surface((pWidth*tileSize, pHeight*tileSize))
    mosaic.fill((0, 0, 0))
    for x in range(0, pWidth):
        for y in range(0, pHeight):
            color = picture.get_at((x, y))
            picture = scan_pictures(color, directory, accuracy)
            # scale selected picture to appropriate proportions
            picture = pygame.transform.smoothscale(picture, \
                                                   (tileSize, tileSize))
            mosaic.blit(picture, (x*tileSize, y*tileSize))
    return mosaic

def main(accuracy, tileSize):
    parser = argparse.ArgumentParser( \
        description='Generate a mosaic out of pictures')
    parser.add_argument('picture', \
                        help='the picture you want to turn into a mosaic')
    parser.add_argument('-t', '--tiles', \
                        help='directory to load tiles from',
                        action='store_true')
    args = parser.parse_args()
    #try:
    if True:
        picture = pygame.image.load(args.picture)
        mosaic = None
        if args.tiles:
            mosaic = generate_mosaic(picture, tileSize, args.tiles, accuracy)
        else:
            mosaic = generate_mosaic(picture, tileSize, '.', accuracy)
        pygame.init()
        screen = pygame.display.set_mode( \
                                         (mosaic.get_width(), \
                                          mosaic.get_height()), \
                                         pygame.HWSURFACE|pygame.DOUBLEBUF)
    
        clock = pygame.time.Clock()
        going = 1
        while going:
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    going = False
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        going = False
            screen.fill((0, 0, 0))
            time = clock.tick(10)/1000.
            pygame.display.set_caption('fps: '+str(clock.get_fps()))
            pygame.display.flip()
    #except:
    if True:
        print('Picture does not exist. Quitting...')
    pygame.quit()
    return

if __name__ == '__main__':
    accuracy = 0.8
    tileSize = 16
    main(accuracy, tileSize)
