"""
Render junit reports as HTML
"""
from jinja2 import Environment, PackageLoader, select_autoescape
import json

class HTMLReport(object):
    def __init__(self):
        self.title = ""
        self.report = None

    def load(self, report, title="JUnit2HTML Report"):
        self.report = report
        self.title = title

    def __iter__(self):
        return self.report.__iter__()

    def __str__(self) -> str:
        env = Environment(
            loader=PackageLoader("junit2htmlreport", "templates"),
            autoescape=select_autoescape(["html"])
        )

        template = env.get_template("report.html")
        return template.render(report=self, title=self.title)


class HTMLMatrix(object):
    def __init__(self, matrix):
        self.title = "JUnit Matrix"
        self.matrix = matrix

    def __str__(self) -> str:
        env = Environment(
            loader=PackageLoader("junit2htmlreport", "templates"),
            autoescape=select_autoescape(["html"])
        )

        template = env.get_template("matrix.html")
        return template.render(matrix=self.matrix, title=self.title)


class HTMLMatrixJson(object):
    def __init__(self, matrix):
        self.title = "JUnit Matrix"
        self.matrix = matrix

    def __str__(self) -> str:
        env = Environment(
            loader=PackageLoader("junit2htmlreport", "templates"),
            autoescape=select_autoescape(["html"])
        )

        result = {"stats": {}, "result": []}
        template = env.get_template("matrix.html")
        stats = []
        for outcome in self.matrix.result_stats:
            stats.append({ outcome.title(): self.matrix.result_stats[outcome]})
        result["stats"] = stats

        print(result)
        report_names = self.matrix.report_order()
        n_reports = len(report_names)
        result_data = []       
        for classname in self.matrix.classes:
          for casename in self.matrix.casenames[classname]:
            xcase = self.matrix.cases[classname][casename]
            for n in range(n_reports):
              axis = report_names[n]
              result_data.append({
                  "class_name": classname,
                  "test_case": casename,
                  "result": self.matrix.combined_result_list(classname, casename)[1],
                  "status": self.matrix.short_outcome(xcase[axis].outcome()),
                  "report_id": xcase[axis].anchor()
              })
        result["result"] = result_data
        
        return str(result)