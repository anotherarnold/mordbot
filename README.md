Mordbot - A custom Discord bot

Mordbot is a feature rich Discord bot that can do most things you'd want a bot to do; it can assign roles using single click commands, supports custom commands, and has chatbot functionality. Usage is simple and easy, mostly being self-explanitory using the built-in help function.

Implementation is mostly straightforward, with chatbot functions being implemented using Markovify and most everything else being done with the Discord.py packages. 

To use Mordbot yourself, you'll need to get an API token from a Discord developer account, which is easy to do. 

Commands are prefixed with the ! character. To get started, attach your API token to Mordbot (the TOKEN variable) and invite it into a server. The !help command should get you started on what it can do and how to use it.

An important note about Mordbot (or bots in general) is that automating role distribution should be handled with care. Within a Discord server's settings, Mordbot can apply any role you tell it about that is lower than its own role within the role list. This means that Mordbot is fully capable of distributing roles with moderator privileges, if you allow it to do so. For this reason it is very important that you A) do not add any roles to Mordbot with moderator powers and B) move Mordbot's role below roles with moderator powers within your server settings. 
