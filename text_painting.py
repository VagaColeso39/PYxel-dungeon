import pygame

def num_painting(text) -> pygame.Surface:
    nums = [pygame.image.load(f'assets/sprites/{i}.png') for i in range(10)]
    nums = list(map(lambda x: pygame.transform.scale(x, (x.get_width()*10, 50)), nums))
    width = 0
    for i in text:
        width += nums[int(i)].get_width()
    width += 10 * (len(text)-1)
    ret = pygame.Surface((width, 50))
    width = 0
    for i in text:
        ret.blit(nums[int(i)], (width, 0))
        width += nums[int(i)].get_width()+10
    return ret
    