TTI Power supply
==================

**Driver for the TTI QL355P power supply**

*Charles Baynham 2023*

This package defines the `TTIPowerSupply` and `TTIPowerSupplyTCP` objects, for
USB and LAN control. Use them e.g. like this::

    d_USB = TTIPowerSupply(id="COM45")
    d_LAN = TTIPowerSupplyTCP(id="10.0.0.0")

    print(d_LAN.get_identity())
