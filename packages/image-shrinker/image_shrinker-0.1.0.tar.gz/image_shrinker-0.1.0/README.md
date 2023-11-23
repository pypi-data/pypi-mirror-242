# image-shrinker

Go directly to the [DOCUMENTATION](https://image-shrinker.readthedocs.io/).

## Description
Yup, you guessed right, it shrinks images.
Use it before committing large image files into git and/or using large image files on a website.

*image-shrinker* was built to scratch my own itch.
You might have the same itch.

- I needed a no-brainer command I could quickly run on the source files of my website(s).
- It would shrink large image files before I committed them to git ... and before I would
  deploy them on my website.
- It wouldn't require me to remember which directories need what kind of shrinking.
  - For example, that images in my `img/thumbnails` directory needed to shrink to width=100
  - But that images in my `img/photos/carousel` needed to shrink to height=300
    so that they were all the same height on my home page's rotating photo carousel.
- I wanted to run the command only once and have it handle multiple shrink cases.
- I wanted all my shrinking requirements specified in a file in my repository
  version-controlled and in sync with the rest of my source files.
- ~~Easy peasy~~ (no, I hate that phrase)

*image-shrinker* happens to be written in Python,
but you do not need to be a Python programmer to use it.

## Documentation
For instructions on how to install and use *image-shrinker*,
see [image-shrinker.readthedocs.io](https://image-shrinker.readthedocs.io/).

## Support
Try opening an issue [HERE](https://gitlab.com/parakin/image-shrinker/-/issues).
No promises on any level of service. Best efforts only.
The code is really simple. Any Python developer should be able to help you.

## Contributing
Contributions will be considered.

## Acknowledgment
Thanks to [Pillow](https://pillow.readthedocs.io/en/stable/), the Python Image Library.
It does all the hard work of shrinking images.

## License
MIT Licensed. See [LICENSE](LICENSE).

## Project status
Actively but lightly maintained by Don Parakin.
