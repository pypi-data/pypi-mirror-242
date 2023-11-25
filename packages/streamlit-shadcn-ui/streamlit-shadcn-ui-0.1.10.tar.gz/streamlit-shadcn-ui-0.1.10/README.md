# streamlit-shadcn-ui :construction:

> streamlit-shadcn-ui is in early development, the updates is shipped frequently. A relative stable will be launched after 11/27 2023. Follow the developer on twitter for updates: ![Follow ob12er](https://img.shields.io/twitter/follow/ob12er)


[![PyPI - Version](https://img.shields.io/pypi/v/streamlit-shadcn-ui)](https://pypi.org/project/streamlit-shadcn-ui/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/streamlit-shadcn-ui)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://shadcn.streamlit.app/)

Using shadcn-ui components in streamlit

<img width="1447" alt="shadcn-demo" src="https://github.com/ObservedObserver/streamlit-shadcn-ui/assets/22167673/ae981a9e-6238-467e-a074-a335e6b9af55">


## Installation

```bash
pip install streamlit-shadcn-ui
```

example:
```py
import streamlit_shadcn_ui as ui
trigger_btn = ui.button(text="Trigger Button", key="trigger_btn")

ui.alert_dialog(show=trigger_btn, title="Alert Dialog", description="This is an alert dialog", confirm_label="OK", cancel_label="Cancel", key="alert_dialog1")

```

## Components

Check docs and compoenent examples in [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://shadcn.streamlit.app/)

+ [x] button
+ [x] checkbox
+ [x] select
+ [x] tabs
+ [x] card
+ [x] avatar
+ [x] date_picker
+ [ ] date_range_picker
+ [x] table
+ [x] input
+ [x] slider
+ [x] textarea
+ [x] switch
+ [x] radio_group
+ [x] alert_dialog
+ [x] hover_card
+ [x] badges
+ [x] link_button

# License
This repo is under MIT license. See [LICENSE](LICENSE) for details.
`streamlit_shadcn_ui/components/packages/streamlit-components-lib` is under its original Apache-2.0 license. It is a temporal patch for streamlit-components-lib in react 18. 
