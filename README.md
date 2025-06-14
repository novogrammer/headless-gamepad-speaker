# Headless Gamepad Speaker

This project provides a small Python application that speaks the current
weather or time when you press buttons on a gamepad. It relies on
`pygame` for input handling and can use either the `say` command on
macOS or `open_jtalk` with `aplay` on Linux to produce speech.

## Requirements

- Python 3.11 or later
- `pygame` (see `requirements.txt`)
- One of the following speech systems:
  - The `say` command (macOS)
  - `open_jtalk` and `aplay` (Ubuntu/Debian)

For Docker usage, see the provided `Dockerfile` which installs the
necessary packages including a dummy sound device via `pulseaudio`.

## Usage

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Ensure your system has either `say` or `open_jtalk` + `aplay`.
3. Connect a gamepad and run the main program:

   ```bash
   python main.py
   ```

4. Press gamepad button **0** to hear the current time or button **1** to
   hear today's weather for Osaka (configured in `weather.py`).

## Customization

Weather forecasts are fetched from the Japan Meteorological Agency. You
can change the area by modifying `AREA_CODE` and `AREA_NAME` in
`weather.py`.

## License

This project is distributed under the MIT License.
