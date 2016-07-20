import ROOT
import style

class BlackHole(object):
    """call blackhole.anything = object to make sure object won't be deleted until blackhole is"""
    def __init__(self):
        self.__dict__["cache"] = []
    def __setattr__(self, name, attr):
        self.store(attr)
    def store(self, object):
        self.cache.append(object)

def mergeplots(outfilename, *infilenames):
    multigraph = ROOT.TMultiGraph()
    legend = ROOT.TLegend(.6, .4, .9, .8)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    b = BlackHole()
    files = []
    for filename in infilenames:
        f = b.f = ROOT.TFile.Open(filename)
        c = b.c = f.c1
        mg = b.m = c.GetListOfPrimitives()[1]
        l = b.l = c.GetListOfPrimitives()[2]
        for g in mg.GetListOfGraphs():
            multigraph.Add(g)
        for entry in l.GetListOfPrimitives():
            legend.AddEntry(entry.GetObject(), entry.GetLabel(), entry.GetOption())
            print entry.GetLabel()
        print list(multigraph.GetListOfGraphs())
    c1 = ROOT.TCanvas()
    multigraph.Draw("APE")
    legend.Draw()
    for ext in "png eps root pdf".split():
        outfilename = outfilename.replace("."+ext, "")
    for ext in "png eps root pdf".split():
        c1.SaveAs(outfilename+"."+ext)


if __name__ == "__main__":
    mergeplots("~/www/TEST/test.png", "fractionClosureQGL.root", "fractionClosure_.root")
