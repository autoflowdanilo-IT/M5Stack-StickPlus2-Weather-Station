# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-05-24

### Added
- Live dashboard with temperature, humidity and barometric pressure
- Dew point calculation (Magnus formula)
- Heat index / feels like calculation
- Pressure trend indicator (rising ^ / stable = / falling v)
- 3-page UI navigated via BtnA
- Max records page tracking peak temperature, humidity and pressure
- Max records reset via BtnB hold with audio feedback
- System info page showing battery level and session uptime
- Battery bar indicator at top of screen (green > 30%, red <= 30%)
- Screen power saving: BtnA hold toggles display on/off
- Hint bar at bottom of each page showing button controls
- Separator lines between data sections for readability
- I2C on Grove port pins SDA=32, SCL=33 for M5StickC Plus
