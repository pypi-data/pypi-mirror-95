# briar_repl

async python repl cli chat client, to be used with briar-headless:

https://code.briarproject.org/briar/briar/tree/master/briar-headless

## usage:

### currently it features:

* contact listing
* contact adding
* contact removing
* contact renaming
* contacts pending list
* contacts display online status
* contacts display unread message count (currently per session only)
* direct chat with contacts
* briar link display
* command help

### two modes:

* command mode (blue bottom bar)
* chat mode    (green bottom bar)

commands in chat mode are called by pre-pending `/` so a `/back` or `/exit_chat` brings you back to command mode

commands are auto completed thanks to the amazing prompt_toolkit package:

https://github.com/prompt-toolkit/python-prompt-toolkit

## installation:

### install via pip:

needs python3.7 or higher:
`python3 -m pip install briar_repl`

briar-headless.jar (1.2.12 or higher) would need to be available in:

`~/.briar/headless/briar-headless.jar`


### install via flatpak

needs flatpak and flatpak builder, briar-headless is bundled in the flatpak.

##### build flatpak

with supplied yaml instructions:
`flatpak-builder --repo=build/flatpak/repo --install-deps-from=flathub --user --force-clean build/flatpak/build org.briarproject.briar_repl.yaml`

##### build flatpak bundle

creates a flatpak file here: `build/briar_repl.flatpak`
`flatpak build-bundle build/flatpak/repo build/briar_repl.flatpak org.briarproject.briar_repl`

##### install flatpak

install flatpak on current machine
`flatpak install --user build/briar_repl.flatpak`

##### run the flatpak

`flatpak run org.briarproject.briar_repl`
