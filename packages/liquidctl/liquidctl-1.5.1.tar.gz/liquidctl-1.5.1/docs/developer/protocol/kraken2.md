# NZXT Kraken X2 and M2 coolers

## Capabilities by model and firmware version

| Model | Firmware versions | Coolant temperature | Static fan/pump control | Dynamic fan/pump control | Illumination control |
| :-- | :-: | :-: | :-: | :-: | :-: |
| M22 | all | no | no | no | yes |
| X[4-7]2 | < 3.0.0 | yes | yes | no | yes |
| X[4-7]2 | ≥ 3.0.0 | yes | instantaneous<sup>1</sup> | yes<sup>2</sup> | yes |

<sup>1</sup> After 5-10 seconds (FIXME) static fan/pump speeds are overridden
by the previously set fan/pump curves.
<sup>2</sup> Dynamic fan/pump curves based on the coolant temperature.

## USB & USB HID descriptors

TODO.

## Types of exchanges

TODO.

## Initialization

No-op.

## Retrieving status information

The cooler sends 16-byte status reports twice a second.

| Raw report slice | Description |
| :-: | :-- |
| 0x0 | Report ID: 0x04 |
| 0x1 | Coolant temperature, integer part, 1/9 °C |
| 0x2 | Coolant temperature, decimal part, 0.1 °C (FIXME) |
| 0x3–0x4 | Fan speed, big endian 2-byte integer, rpm |
| 0x5–0x6 | Pump speed, big endian 2-byte integer, rpm |
| 0xb | Firmware version, major number |
| 0xc–0xd | Firmware version, big endian 2-byte integer, minor number<sup>3</sup> |
| 0xe | Firmware version, patch number |

Only Kraken X models return valid coolant temperature, fan speed or pump speed
values.

<sup>3</sup> The minor number of the firmware version is *presumed* to be
specified as a 2-byte integer, but the second byte has not been necessary yet.

Something like would (sort of) make sense, but is *not* what is done.

----- TS -----    ------ PROTOCOL ------
bits  fraction -> fraction  bits  bits+1
--------------    ----------------------
000     0.000  ->   0.000    000     001
001     0.125  ->   0.111    001     010
010     0.250  ->   0.222    010     011
011     0.375  ->   0.333    011     100
100     0.500  ->   0.555    101     110
101     0.625  ->   0.666    110     111
110     0.750  ->   0.777    111    1000
111     0.875  ->   0.888   1000    1001

32 (0x20)    123456789
33 (0x21)    1234 6789
34 (0x22)    123456789
35 (0x23)    1234 6789
36 (0x24)    12 45 789
37 (0x25)    1234 6789
38 (0x26)    12 45 789
39 (0x27)    12 45 789
