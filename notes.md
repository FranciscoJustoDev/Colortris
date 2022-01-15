# Colortris
>
>## Preparing for graphics
>
> - load graphics in Load_data.  
> - monster sprites should be a list containing lists  
> holding all  for a monster type (4 types!).  
>
> - spawn function passes type's respective sprites  
> as monster constructor parameter:  
>
>> - every monster handles 1 set of sprites/animations  
>> that correspond to own type!  
>> (this means no handling of unnecessary data)  
>> - each object handles/references animations the same way,  
>> so every sprite data should follow the same rules.  
>>
>>> Example:  
>>>
>>> - "ghost" type sprite_data is a list.  
>>> - each element is a ghost_image/image_reference.  
>>>
>>>> - 0 to 2 are the 3 sequential sprites for the  
>>>> "falling" animation.  
>>>> - 3 to 5 are the sprites for the "alone" animation.  
>>>> the rest of the animations follow the same  
>>>> organizational structure.  
>>>
>>> - when referencing a specific animation of any object this way,  
>>> we can simply call the animation we want and the object  
>>> plays it, no matter its type!  
>
> - fix offset when a sped up chip comes to a halt.  
> - make shure chip position handling is done  
> always from *rect.center*.  
>
>>## Preparing for graphics - Done
>
> - RENAME CHIP SPRITE OBJECT TO MONSTER!!  
> - monster type identifier _integer 1-4_ should be  
> passed as a parameter by spawn function.  
>
>## To Do
>
> - sfx and music - sfx manager.  
> sound effect for landing, score a point,  
> button select in menu.  
>
>> - graphics, vfx and animation manager.  
>> - level backgrounds - animated.  
> monster sprites - 4 monster types:  
> falling  
> alone animation (always grounded).  
> has neighbour:  
> grounded, above clear  
> grounded, above filled  
> above, above cleared  
> above, above filled  
> has match:  
> grounded, above clear  
> grounded, above filled  
> above, above cleared  
> above, above filled  
>
> landing sfx, floating hearts sfx, dissappear sfx
>
> - start and game over menus.  
> - score and high score - dynamic interface.  
> font to use  
> saving system for username and user's highscore.  
> scoreboard (mby embedded in GO Menu).  
>
## Fix / Handle
>