# https://www.youtube.com/watch?v=qL2g5YIVick&ab_channel=TechToTinker

def mount_sd(folder = "/sd"):
    import os
    from machine import Pin, SoftSPI
    from utils.modules.sdcard import SDCard

    """
    pin assignment
    vcc -> 5v
    gnd -> gnd
    miso -> gpio 13
    mosi -> gpio 12
    sck -> gpio 14
    cs -> gpio 25

    """

    spisd = SoftSPI(
        -1,
        miso = Pin(13),
        mosi = Pin(12),
        sck = Pin(14)
    )
    sd = SDCard(spisd, Pin(25))

    vfs = os.VfsFat(sd)
    os.mount(vfs, folder)
    #os.chdir("sd")
    #print("sd card contains:", os.listdir())
    print(f"mounted sd card in '{folder}'")

if __name__ == "__main__":
    mount_sd()

