import pygame

def num_painting(text, height) -> pygame.Surface:
    nums = [pygame.image.load(f'assets/sprites/{i}.png') for i in range(10)]
    nums = list(map(lambda x: pygame.transform.scale(x, (int(x.get_width()*height/5), height)), nums))
    dot = pygame.image.load('assets/sprites/..png')
    dot = pygame.transform.scale(dot, (int(dot.get_width()*height/5), height))
    width = 0
    for i in text:
        width += nums[int(i)].get_width()  if i!='.' else dot.get_width()
    width += 10 * (len(text)-1)
    ret = pygame.Surface((width, height))
    width = 0
    for i in text:
        ret.blit(nums[int(i)] if i!='.' else dot, (width, 0))
        width += (nums[int(i)].get_width()+10) if i!='.' else dot.get_width()+10
    return ret
    