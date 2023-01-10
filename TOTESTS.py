import player
import items

hero = player.Player()
print(hero.__dict__)
hero.pick_up(items.FirstTestItem('first', stackable=True))
print(hero.__dict__)
hero.pick_up(items.SecondTestItem('second'))
print(hero.__dict__)
for i in range(18):
    print(hero.pick_up(items.FirstTestItem(f'first{i}', quantity=6, stackable=True)))
print(hero.__dict__)