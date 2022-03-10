# SVGReplicate 

Tool for batch modifying and replicating SVG files. 

## Installation 

Install from PyPI by running `pip install svgreplicate`.

## Usage

Create an SVG file, either by hand or with your favorite vector graphics tool, like [InkScape](https://inkscape.org):

```xml
<svg
    width="210mm"
    height="297mm" 
    id="svg" 
    version="1.1"
    xmlns="http://www.w3.org/2000/svg" >
    <g id="group1">
        <ellipse
            style="opacity:1;fill:#009bff"
            id="ellipse1"
            cx="0.0"
            cy="0.0"
            rx="10.0"
            ry="10.0" />
        <g id="group2" />
    <text id="text1">
        <tspan>First text</tspan>
        <tspan>Second text 
            <tspan>Nested text</tspan> 
        </tspan>
    </text>
    </g>
</svg>
```

Next, create a json with the replicas you want: 

```json
[
    {
        "filename": "example/replica1.svg", 
        "modifications": [
        	{"id": "ellipse1", "style": {"fill": "#000000", "display": "none"}},
        	{"id": "group2", "style": {"display": "none"}},
        	{"id": "text1", "text": "Hello, world!"}
        ]
    },
    {
        "filename": "example/replica2.svg",
        "modifications": [
                {"id": "ellipse1", "style": {"fill": "#ffffff", "display": "none"}},
                {"id": "group2", "style": {"display": "none"}},
                {"id": "text1", "text": "Here's Johnny!"}
        ]
    }
]
```

And finally, run the script:

```bash 
svgreplicate --filename path-to-svg-template.svg --replicas path-to-replicas-config.json 
```

You now have 2 files in the example folder, based on the template, with the specified modifications. 

## Backlog 

In future, I'd like to add at least the functionality for automatically rendering to PNG. 

