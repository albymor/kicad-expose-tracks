import pcbnew
import wx
import os


class Dialog(wx.Dialog):
    def __init__(self, parent, msg):
        wx.Dialog.__init__(self, parent, id = -1, title = "Expose Tracks")
        panel = wx.Panel(self)
        message = wx.StaticText(panel, label = msg)

    def OnClose(self, e):
        e.Skip()
        self.Close()

def show_message(msg):
    dialog = Dialog(None, msg)
    dialog.ShowModal()
    dialog.Destroy()

def get_selected_track(tracks):
    return [t for t in tracks if  t.IsSelected()]

class ExposeTracks(pcbnew.ActionPlugin):
    def defaults(self):
        self.name                = "Expose Tracks"
        self.category            = "Wiring"
        self.description         = "Expose copper tracks"
        self.show_toolbar_button = True
        self.icon_file_name      = os.path.join(os.path.dirname(__file__), "icon.png")

    def Run(self):
        self.pcb = pcbnew.GetBoard()
        tracks   = self.pcb.GetTracks()

        selected_tracks = get_selected_track(tracks)
        if len(selected_tracks) == 0:
            show_message("Error: No track selected")
            return

        for trk in selected_tracks:
            start = trk.GetStart() 
            end = trk.GetEnd()

            t = pcbnew.PCB_SHAPE(self.pcb)
            t.SetShape(pcbnew.S_SEGMENT)
            t.SetWidth(trk.GetWidth())
            if trk.GetLayer() == pcbnew.F_Cu:
                t.SetLayer(pcbnew.F_Mask)
            else:
                t.SetLayer(pcbnew.B_Mask)
            t.SetStart(start)
            t.SetEnd(end)
            self.pcb.Add(t)
