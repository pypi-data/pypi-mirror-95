# DISCLAIMER!
### This package is only vaguely tested.

# Installing
### Python 3.6 or higher is required
other than that it's just as simple as
```
pip install discord.py-embed-wrapper
```
```python
from embed_wrapper import *
```

# Wrapper Classes - Examples/Usage
### EmbedField
to create an `EmbedField` object
```python
wrapped_field = EmbedField(name=field_name, value=field_value, inline=field_inline)
```

and then use it in the initialisation of an `EmbedWrapper`
### EmbedWrapper
```python
embed_wrapper = EmbedWrapper(
    author_name=author_name, author_url=author_url, author_icon_url=author_icon_url,
    embed_type=embed_type, title=title, url=url, color=color, description=description,
    timestamp=timestamp,
    footer_text=footer_text, footer_icon_url=footer_icon_url,
    image_url=image_url, thumbnail_url=thumbnail_url,
    fields=[wrapped_field]
)
```
to finalize and instantiate the embed from the wrapper call
```python
embed = embed_wrapper.embed
```

# Helper Functions - Examples/Usage
### embeds_from_message
Creates a List of Embeds from a give Message. Returns None if the given Message didn't have any Embeds.
```python
def embeds_from_message(message: Message) -> Optional[List[Embed]]:
    ...

embeds = embeds_from_message(message=message)
```
### send_embed_message
Sends a Message including an Embed to either a Guild TextChannel or a DMChannel and returns the sent Message.
```python
async def send_embed_message(
        embed: Embed,
        invoking_message: Message,
        as_reply: bool = False,
        as_dm: bool = False,
        dm_channel: DMChannel = None,
        pin: bool = False,
        message_content: str = "",
        reactions: List[str] = None,
        mentions: List[Union[User, Member, Role]] = None,
        append_mentions: bool = False
) -> Message:
...
```
simplest usage
```python
embed_message = await send_embed_message(embed=embed, invoking_message=message)
```
Sends an Embed Message only containing the embed in the same channel it was invoked. 
### edit_embed_message
Edits a given Embed Message with a new Embed and optionally new Message Content and returns the edited Message. Pass None as the Embed to remove it.
```python
async def edit_embed_message(
        embed: Embed,
        message: Message,
        message_content: Optional[str],
) -> Message:
...
```
usage
```python
embed_message = await edit_embed_message(embed=embed, message=embed_message)
```

