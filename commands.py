import subprocess

subprocess.run(["pyside2-uic" , "gui/myWindow.ui", "-o" ,"gui/myWindow.py"])

# pyinstaller hyperion.py --onefile
# pyside2-designer


"""
        engine = None
        for e in self.engines:
            if e.name == self.currentEngine:
                engine = e
                break

        if self.checkBox_range.checkState(): # if range of chapter mode
            print("range mode")
            result = engine.download_range_chapters_from_name(manga_name, first_chap, last_chap, output_name, compress = compress_ext)
            print(result)
        else:
            # normal mode, only for a single chapter
            result = engine.download_volume_from_manga_url(manga_url, volume_number, volume_name=output_name, display_only=False, compress = compress_ext)
            if result == False:
                self.set_output_consol("Your volume is not on the website\n try another one or some pictures are missing\n Verify in the download folder")
            elif result == None:
                self.set_output_consol("An error occured")
            else:
                self.set_output_consol("Download of " + manga_name + str(volume_number) + " finished")
            print(result)

"""

