import numpy as np
import tkinter as tk
import tkinter.filedialog
import matplotlib as mpl
from tk_steroids.matplotlib import CanvasPlotter


from .version import __version__
from .spectronator import Spectronator

PLOT_POINT_TARGET = 1000

def downsampled(x, y):
    '''Downsamples a sequence to the PLOT_POINT_TARGET.
    '''
    n_points = len(y) # == len(x)
    
    ratio = int(n_points / PLOT_POINT_TARGET) 
    if ratio <= 1:
        return x, y

    return x[::ratio], y[::ratio]


class OperationPanel(tk.Frame):
    '''Main point of action, "manages" other widgets.
    '''
    
    def __init__(self, parent, spectronator, tv1, tv2, tv3):
        super().__init__(parent)
        
        self.spectronator = spectronator
        self.tv1 = tv1
        self.tv2 = tv2
        self.tv3 = tv3
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        # FILTERING
        self.filtering_frame = tk.LabelFrame(self, text='Data filtering')
        self.filtering_frame.grid(sticky='NSWE', column=0, row=1, rowspan=2)
        self.filtering_frame.columnconfigure(0, weight=1)

        self.openbut = tk.Button(self, text='Open 19-LED file...', command=self.open19)
        self.openbut.grid(row=0, column=0) 

        tk.Label(self.filtering_frame, text='Lowend pass-frequency (Hz)').grid()
        self.lowpass_slider = tk.Scale(
                self.filtering_frame,
                from_=0.001, to=1, orient=tk.HORIZONTAL, resolution=0.001,
                command=self.refresh_tv2)
        self.lowpass_slider.grid(sticky='WE')
        self.lowpass_slider.set(self.spectronator.lowpass)

        tk.Label(self.filtering_frame, text='Highend pass-frequency (Hz)').grid()
        self.highpass_slider = tk.Scale(
                self.filtering_frame,
                from_=1, to=1000, orient=tk.HORIZONTAL, resolution=1,
                command=self.refresh_tv2)
        self.highpass_slider.grid(sticky='WE')
        self.highpass_slider.set(self.spectronator.highpass)

        tk.Label(self.filtering_frame, text='Filter order').grid()
        self.order_slider = tk.Scale(
                self.filtering_frame,
                from_=1, to=32, orient=tk.HORIZONTAL, resolution=1,
                command=self.refresh_tv2)
        self.order_slider.grid(sticky='WE')
        self.order_slider.set(self.spectronator.filter_order)

        tk.Label(self.filtering_frame, text='Filter').grid()
        self.filter_selection = tk.StringVar(self)
        self.filter_selection.set(self.spectronator.filter)
        self.filter_optionmenu = tk.OptionMenu(
                self.filtering_frame,
                self.filter_selection, *list(self.spectronator.filters.keys()),
                command=self.refresh_tv2)
        self.filter_optionmenu.grid()


        # ANALYSIS
        self.analysis_frame = tk.LabelFrame(self, text='Analysis')
        self.analysis_frame.grid(sticky='NSWE', column=1, row=1)
        self.analysis_frame.columnconfigure(0, weight=1)

        tk.Label(self.analysis_frame, text='(Duration + pause) / per LED (s)').grid()
        self.duration_slider = tk.Scale(
                self.analysis_frame,
                from_=0, to=20, orient=tk.HORIZONTAL, resolution=0.1,
                command=self.refresh_tv2)
        self.duration_slider.grid(sticky='WE')
        self.duration_slider.set(7)
        

        tk.Label(self.analysis_frame, text='Method').grid()
        self.method_selection = tk.StringVar(self)
        self.method_selection.set(self.spectronator.method)
        self.method_optionmenu = tk.OptionMenu(
                self.analysis_frame,
                self.method_selection, *self.spectronator.methods,
                command=self.refresh_tv2)
        self.method_optionmenu.grid()



    def open(self, title):
        return tkinter.filedialog.askopenfilename(title=title)

    def open19(self, fn=None):
        if fn is None:
            fn = self.open('Select a 19-LED file (CSV or .mat)')
        
        if not fn:
            return
        
        self.spectronator.clear()
        self.spectronator.add_datafile(fn, [364, 377, 394, 405, 419, 437, 452,
                               470, 485, 518, 534, 544, 560, 576,
                               590, 618, 629, 680, 693])
        
        self.highpass_slider.config(to=self.spectronator.max_fs)
        self.refresh_tvs()

    def refresh_tvs(self, *args):

        self.tv1.clear()
        fig, ax = self.tv1.plotter.get_figax()
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Voltage (mV)')


        X, Y = self.spectronator.get_raw() 
        for x,y in zip(X,Y):
            self.tv1.plot(*downsampled(x,y))

        self.refresh_tv2()

    def refresh_tv2(self, *args):

        self.tv2.clear()
        fig, ax = self.tv2.plotter.get_figax()
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Voltage (mV)')

       
        self.spectronator.lowpass = float(self.lowpass_slider.get())
        self.spectronator.highpass = float(self.highpass_slider.get())
        self.spectronator.filter_order = float(self.order_slider.get())
        self.spectronator.filter = str(self.filter_selection.get())

        X, Y = self.spectronator.get_filtered() 
        for x,y in zip(X,Y):
            self.tv2.plot(*downsampled(x,y))

        # Draw chop lines
        self.spectronator.chop_interval = float(self.duration_slider.get())
        points = self.spectronator.get_choppoints()

        maxy = np.max(Y[::100])
        miny = np.min(Y[::100])

        segmentsx = []
        segmentsy = []
        for i in range(len(points)):
            segmentsx.append([points[i], points[i]])
            segmentsy.append([miny, maxy])

        self.tv2.plot(np.array(segmentsx).T, np.array(segmentsy).T, color='red')

        #for xp in points:
        #    self.tv2.plot([xp, xp], [miny, maxy])

        self.refresh_tv3()

    def refresh_tv3(self, *args, XY=None):
        
        self.tv3.clear()
        fig, ax = self.tv3.plotter.get_figax()
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Response (mV)')

        self.spectronator.method = self.method_selection.get()
        X, Y = self.spectronator.get_spectral_response()
        
        #X, Y = self.spectronator.get_filtered()

        for x,y in zip(X,Y):
            self.tv3.plot(x,y)
       


class ExportPanel(tk.LabelFrame):

    def __init__(self, parent, spectronator, tv1, tv2, tv3):
        super().__init__(parent, text='Export')
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.spectronator = spectronator
        self.tvs = {'original': tv1, 'filtered': tv2, 'sensitivity': tv3}

        for itv, tv in enumerate(self.tvs):
            tk.Button(self,
                      text=f'{tv.capitalize()} CSV',
                      command=lambda name=tv: self.export_csv(name)
                      ).grid(row=0, column=itv)
            tk.Button(self,
                      text=f'{tv.capitalize()} PNG',
                      command=lambda name=tv: self.export_image(name)
                      ).grid(row=1, column=itv)

    def export_csv(self, tvname):
        if tvname == 'sensitivity':
            X, Y = self.spectronator.get_spectral_response()
        elif tvname == 'filtered':
            X, Y = self.spectronator.get_filtered()
        elif tvname == 'original':
            X, Y = self.spectronator.get_raw()
        else:
            raise ValueError(f'Unkown tvname: {tvname}')

        data = np.vstack((X[0],Y[0])).T

        fn = tkinter.filedialog.asksaveasfilename(
                title=f'Save CSV ({tvname})',
                initialfile=f'{tvname}.csv')
        if fn:
            np.savetxt(fn, data, delimiter=',')


    def export_image(self, tvname, ending='.png'):
        
        tv = self.tvs.get(tvname)

        fn = tkinter.filedialog.asksaveasfilename(
                title=f'Save image ({tvname})',
                initialfile=f'{tvname}{ending}')
        if not fn:
            return
        
        fig, ax = tv.plotter.get_figax()
        fig.savefig(fn)

class TraceView(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.plotter = CanvasPlotter(self) 
        self.plotter.grid(sticky='NSWE')

    def plot(self, *args, **kwargs):
        self.plotter.plot(*args, ax_clear=False, **kwargs)

    def clear(self):
        self.plotter.ax.clear()
        self.plotter.canvas.draw()






def main():
    app = tk.Tk()
    app.title(f'SpectroNator - v{__version__}')
    app.geometry('800x600')

    app.columnconfigure(0, weight=1)
    app.columnconfigure(1, weight=1)
    app.rowconfigure(0, weight=1)
    app.rowconfigure(1, weight=1)

    tv1 = TraceView(app)
    tv1.grid(sticky='NSWE', row=0, column=1)
    
    tv2 = TraceView(app)
    tv2.grid(sticky='NSWE', row=1, column=1)

    tv3 = TraceView(app)
    tv3.grid(sticky='NSWE', row=1, column=0)

    spectronator = Spectronator()

    opanel = OperationPanel(app, spectronator, tv1, tv2, tv3)
    opanel.grid(sticky='NSWE', row=0, column=0)
    
    epanel = ExportPanel(opanel, spectronator, tv1, tv2, tv3)
    epanel.grid(sticky='NSWE', row=2, column=1)



    app.mainloop()


if __name__ == "__main__":
    main()
