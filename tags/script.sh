#/usr/bin/bash

# Starting from: https://docs.google.com/document/d/1JUxmoFqygjWYoDIKcpTh1Ld7kHIH0kWqbaMfZL4EuJw/edit

convert -rotate 90 -density 300 -depth 8 -quality 100 -crop 2500x1666+700+0 Tags.pdf out.png
