<h1 align="center">
  <a href="https://movary.org"><img src="https://github.com/leepeuker/movary/raw/main/public/images/movary-logo-192x192.png" height="160px" width="160px"></a>
  <br>
  Movary - Kodi Addon
  <br>
</h1>

<h4 align="center">The official Movary Kodi Addon for automatic movie plays logging</h4>

<p align="center">
<a href="https://github.com/leepeuker/movary-kodi-addon" target="_blank" rel="noopener noreferrer"><img src="https://img.shields.io/github/stars/leepeuker/movary-kodi-addon?style=flat&color=yellow&label=github%20stars" ></a>
<a href="https://github.com/leepeuker/movary-kodi-addon/issues" target="_blank" rel="noopener noreferrer"><img src="https://img.shields.io/github/issues/leepeuker/movary-kodi-addon?color=eba434&label=github%20issues" ></a>
<a href="https://discord.gg/KbcSqggrgW" target="_blank" rel="noopener noreferrer"><img src="https://img.shields.io/discord/1125830398715363399" ></a>
<a href="https://github.com/leepeuker/movary-kodi-addon/blob/main/LICENSE" target="_blank" rel="noopener noreferrer"><img src="https://img.shields.io/github/license/leepeuker/movary-kodi-addon" ></a>
</p>

[Movary](https://github.com/leepeuker/movary) is a free and open source web application to track, rate and explore your movie watch history.
This is a Kodi addon to automatically log your finished movie plays in Kodi to your Movary server.

## Documentation

### Requirements

- **Webhook URL**: A Kodi Webhook URL from Movary (generated in Movary)

### How to install

Download the addon:

- Option 1: Download the "Source code (zip)" of a [release](https://github.com/leepeuker/movary-kodi-addon/releases/tag)
- Option 2: Download the repository as a zip ([how to](https://docs.github.com/en/repositories/working-with-files/using-files/downloading-source-code-archives#downloading-source-code-archives-from-the-repository-view))

Than go into Kodi to "Settings -> Add-ons -> Install from zip file" and select the downloaded zip file to install it.

Afterwards go to "Settings -> My add-ons -> Services -> Movary -> Configure" and make sure to enter your Movary webhook url and to enable the webhook. 

### Development

Create an installable addon zip locally from the currently checked-out commit:
```
git archive --format=zip  --prefix=movary-kodi-addon/ --output=movary-kodi-addon.zip HEAD
```

## Support

- Please report bugs and request features/changes via [Github issues](https://github.com/leepeuker/movary-kodi-addon/issues/new/choose)
- Ask for help or discuss related topics via [Github discussions](https://github.com/leepeuker/movary-kodi-addon/discussions)
- Join our [Discord server](https://discord.gg/KbcSqggrgW)

## Contributors

* [@leepeuker](https://github.com/leepeuker) as Lee Peuker
