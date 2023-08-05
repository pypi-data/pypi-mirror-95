import pandas as pd
import sympy as sp
import numpy as np
from .units import unit
import os
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from . import extra_funcs as ef

exval, exUnis = {}, {}


# %%

class table:
    """
    The table class is the core of this package. Each table object contains
    columns of data most often imported from a .xlsx file of .csv like file.

    To initialize as table object, simply give it the name of the file you wish
    to import data from.

    ex:
    import data_table as
    """
    def __init__(self, datname, AutoInsert=False, units={}, formules={},
                 sheet=None, data=None, delimiter=','):
        self.units = units
        if data is not None:
            if isinstance(data, pd.DataFrame):
                self.data = data
            else:
                self.data = pd.DataFrame(data)
        elif os.path.isfile(datname + ".xlsx"):
            self.data = pd.read_excel(datname + ".xlsx", sheet_name=sheet)
        elif os.path.isfile(datname + ".csv"):
            self.data = pd.DataFrame(np.genfromtxt(
                datname + ".csv", delimiter=delimiter, names=True))
        else:
            print("Le fichier {} n'as pas été trouvé :(".format(datname))
        self.giveUnits(units)
        self.formulas = {}

        if AutoInsert:
            lol = True
            while lol:
                lol = False
                for i in range(len(self.data.columns) - 1):
                    if not ef.isUncertain(self.data.columns[i]) and\
                       not ef.isUncertain(self.data.columns[i + 1]):
                        self.data.insert(i + 1, ef.delt(self.data.columns[i]),
                                         [0 for i in range(len(self.data))])
                        lol = True

            if not ef.isUncertain(self.data.columns[-1]):
                self.data.insert(len(self.data.columns), ef.delt(
                    self.data.columns[-1]), [0 for i in range(len(self.data))])

    def __repr__(self):
        dat = [c for c in list(self.data) if 'Delta' not in c]
        return str(self.data[dat])

    def __getitem__(self, x):
        return np.array(self.data[x])

    def __len__(self):
        return len(self.data)

    def __setitem__(self, c, v):
        self.data[c] = v

    def newCol(self, name, expression, extra=None, pos=None, NoIncert=False,
               units=None):
        """
        This methode allows you to add a new columns to your table given a
        certain formula. The uncertainty on the new values and units will be
        automatically taken care of.

        ex:
        >>> dt = table("foo")
        >>> dt
        ...     bar   baz
        ... 0   0.0  1.00
        ... 1   1.0  0.50
        ... 2   6.0  0.90
        ... 3   7.0  0.60
        ... 4   8.0  0.01
        ... 5   9.0  3.00
        ... 6  12.0  6.30
        ... 7  15.0  8.90

        >>> dt.newCol('qux', 'bar + baz')
        >>> dt
        ...     bar   baz    qux
        ... 0   0.0  1.00   1.00
        ... 1   1.0  0.50   1.50
        ... 2   6.0  0.90   6.90
        ... 3   7.0  0.60   7.60
        ... 4   8.0  0.01   8.01
        ... 5   9.0  3.00  12.00
        ... 6  12.0  6.30  18.30
        ... 7  15.0  8.90  23.90
        """
        if pos is None:
            pos = len(self.data.columns)
        expression = sp.sympify(ef.preSymp(expression))
        self.formulas[name] = expression

        out = np.empty((len(self.data), 2))

        pre_dict = dict(zip([f"dummy{x}" for x in range(
            len(expression.free_symbols))], map(str, expression.free_symbols)))
        expression = expression.subs({v: k for k, v in pre_dict.items()})
        lamb = sp.lambdify(expression.free_symbols, expression)
        V_dict = self.data[:].to_dict("records")
        if not NoIncert:
            expr_incert = ef.formule_incertitude(self.formulas[name])
            pre_dict_i = dict(zip(
                [f"dummy{x}" for x in range(len(expr_incert.free_symbols))],
                map(str, expr_incert.free_symbols)
                ))
            expr_incert = expr_incert.subs(
                {v: k for k, v in pre_dict_i.items()})
            lamb_incert = sp.lambdify(expr_incert.free_symbols, expr_incert)
        # Le cacul est fait ligne par ligne, probablement très optimisable
        for i in range(len(self.data)):
            vals = V_dict[i]
            vals.update(exval)
            nvals = {name: vals[pre_dict[name]] for name in pre_dict}
            delt_vals = {name: vals[pre_dict_i[name]] for name in pre_dict_i}
            out[i] = [
                lamb(**nvals), 0 if NoIncert else lamb_incert(**delt_vals)]
        # Nomme les colonnes et les ajoute au tableau
        if units:
            self.units[name] = unit(units)
        else:
            self.units[name] = lamb(*(
                self.units[str(i)]
                if str(i) in self.units
                else exUnis[str(i)]for i in self.formulas[name].free_symbols)
                )
        self.data.insert(pos, name, out[:, 0])
        self.data.insert(pos + 1, ef.delt(name), out[:, 1])
        self.fixUnits()

    def delCol(self, names):
        if not isinstance(names, list):
            names = [names]
        for name in names:
            self.data = self.data.drop(columns=[name, ef.delt(name)])

    def giveUnits(self, units):
        for col in self.data.columns:
            try:
                if isinstance(units[col], str):
                    units[col] = unit(units[col])
                self.units[col] = units[col]
            except:
                try:
                    self.units[col] = self.units[col]
                except:
                    self.units[col] = unit("1")

    def changeUnits(self, units):
        for col in units:
            fact = self.units[col].to(units[col])
            self.data[col] *= float(fact)
            self.data[ef.delt(col)] *= float(fact)

    def renomerCols(self, names):
        # vars = list(sp.symbols(noms))
        self.data.columns = [n for var in names.split(" ")
                             for n in (var, ef.delt(var))]

# Combine les colonnes de valeurs et d'incertitude
# applique de la mise en forme des données
    def squish(self):
        out = pd.DataFrame([])
        for col in [str(i) for i in self.data if "Delta" not in str(i)]:
            outCol = []
            # prendre toutes les valeurs + leurs delta individuellement
            for x in range(len(self.data[col])):
                # calculer le nombre de nombre de chiffres significatif requis
                val = abs(self.data[col][x])
                d = self.data[ef.delt(col)][x]
                # formater la colonne en fonction des résultats
                if d == 0:
                    s = str(val)
                    while s.endswith('0') or s.endswith('.'):
                        s = s[:-1]
                    outCol.append("$" + s + "$")
                else:
                    miam = "{{:.{}g}}"\
                          .format(- np.ceil(-sp.log(abs(val), 10))
                                  + np.ceil(-sp.log(d, 10)) + 1).format(val)
                    outCol.append(
                        "$" + miam + " \\pm " + "{:.1g}$"
                        .format(ef.roundUp(self.data[ef.delt(col)][x]))
                        )
            out["$" + col + "$"] = outCol
        return(out)

    # Export un ficher .tex en faisant toutes les modifications nécessaire
    def makeGoodTable(self,name, unite=None):
        try:
            os.mkdir("tableaux")
        except:
            pass
        self.fixUnits()
        exp = self.squish()
        names = []
        for col in self.data.columns[::2]:
            if str(self.units[col].SIval) in ["1", '1.00000000000000']:
                names.append("${}$".format(col))
            else:
                names.append("${}$ ({})".format(col, self.units[col].symb))
        exp.columns = names
        latex = exp.to_latex(index=False)\
            .replace("\\textbackslash ", "\\")\
            .replace("\\_", "_")\
            .replace("\\\\", "\\\\ \\hline")\
            .replace("\\$", "$").replace("e+", "e")\
            .replace("\\toprule", "\\hline")\
            .replace("\\midrule", "")\
            .replace("\\bottomrule", "")\
            .replace('\\textasciicircum', '^')\
            .replace(r'\{', '{')\
            .replace(r'\}', '}')\
            .replace('newton', "N")\
            .replace('$tau', r'$\tau')\
            .replace("l" * len(exp.columns), "|" + "c|" * len(exp.columns))\
            .replace("pourcent", r"\%")\
            .replace("$omega", r"$\omega")
        with open(r"tableaux\{}.tex".format(name), "w+") as final:
            final.write(latex)

    def fixUnits(self):
        for col in self.data.columns[::2]:
            if self.units[col] == 0:
                self.units[col] = unit("1")
            const = self.units[col].exctractConstant()
            self.data[col] *= float(const)
            self.data[ef.delt(col)] *= float(const)
            self.units[col] = unit(str(self.units[col].symb / const))

    # def errorbar(self,a,b):
    #     lol = tuple(self[i] for i in [a,b,delt(b),delt(a)])
    #     plt.errorbar(*lol,".")
    #     plt.xlabel("$"+a+"$ "+"("+str(self.units[a])+")")
    #     plt.ylabel("$"+b+"$ "+"("+str(self.units[b])+")")

    def importCol(self, name, df, index=None):
        if index is None:
            index = (len(self.data) - 1) / 2
        self.data.insert(index * 2, name, df[name], False)
        self.data.insert(index * 2 + 1, ef.delt(name), df[ef.delt(name)], False)

    def plot(self, xn, yn, label=None):
        plt.errorbar(*self[[xn, yn, ef.delt(yn), ef.delt(xn)]].T, ".", label=None)
        plt.xlabel(ef.ax_name(self, xn))
        plt.ylabel(ef.ax_name(self, yn))
        # plt.legend()

    def fit(self, func, xn, yn, show=True, maxfev=1000, **kargs):
        x0 = kargs["x0"] if "x0" in kargs else None
        popt, pcov = curve_fit(func, *self[[xn, yn]].T, x0, maxfev=maxfev)
        if show:
            self.plot(xn, yn, label="Données")
            plt.plot(self[xn], func(self[xn], *popt), label="fit")
            plt.legend()
        return popt, pcov

    def append(self, name, data, incert=None, pos=None, units="1"):
        if pos is None:
            pos = len(self.data.columns)
        if incert is None:
            incert = np.zeros(len(self))
        self.units[name] = unit(units)
        self.data.insert(pos, name, data)
        self.data.insert(pos + 1, ef.delt(name), incert)
        self.fixUnits()


# %%
