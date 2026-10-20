#!/usr/bin/env python

import _thread
import argparse
import os
import re
import sys
import threading
from contextlib import contextmanager
from os.path import isfile, join
from subprocess import PIPE, TimeoutExpired, run


class BaseTask:
    TIME_LIMIT_SECONDS = 1.0
    ABS_TOLERANCE = 0.1

    SPACES_RE = re.compile(r"\s+", re.M)

    def __init__(self, continue_on_error=True, only_matching=None):
        self.continue_on_error = continue_on_error
        self.only_matching = only_matching
        self.tested_cases = set()
        self.passed_cases = set()
        self.tested_units = set()
        self.passed_units = set()
        self.number_cases = 0
        self.show_all_errors = False
        self.python3 = self.find_python3()
        self.runner_ra = None

    def find_python3(self):
        suffix = ".exe" if os.name == "nt" else ""
        for py in ["python3", "python", "py"]:
            for path in os.environ["PATH"].split(os.pathsep):
                exe_file = os.path.join(path, py + suffix)
                if isfile(exe_file):
                    return py
        print("o interpretador python3 não está no path; verifique sua instalação")
        sys.exit(1)

    def read_file_utf8(self, filename):
        assert isfile(filename), f"não existe o arquivo {filename}"
        try:
            with open(filename, encoding="utf-8", errors="strict") as f:
                return f.read()
        except ValueError:
            raise AssertionError(f"encoding inválido em {filename}; por favor, use UTF-8")
        except Exception as e:  # noqa
            raise AssertionError(f"falha ao ler arquivo {filename}: {e}")

    def strip_spaces(self, text):
        return self.SPACES_RE.sub(" ", text.strip())

    def compare_stripped(self, out, res):
        return self.strip_spaces(out) == self.strip_spaces(res)

    @staticmethod
    def get_possible_number(text):
        try:
            return float(text)
        except ValueError:
            return None

    def compare_doubles(self, out, res):
        import math

        out = out.split()
        res = res.split()
        if len(out) != len(res):
            return False
        for a, b in zip(out, res):
            if a == b:
                continue
            a = self.get_possible_number(a)
            b = self.get_possible_number(b)
            if a is None or b is None:
                return False
            if not math.isclose(a, b, abs_tol=self.ABS_TOLERANCE):
                return False
        return True

    def compare_output(self, out, res):
        return self.compare_stripped(out, res)

    def compare_files(self, out, res):
        out = self.read_file_utf8(out)
        res = self.read_file_utf8(res)
        return self.compare_output(out, res)

    def exists(self, filename):
        assert isfile(filename), f"você deve criar um arquivo {filename}"

    def run_binary_inner(self, cmd, stdin, stdout, input):
        if input is None:
            p = run(
                cmd,
                stdin=stdin,
                stdout=stdout,
                encoding="utf8",
                errors="ignore",
                timeout=self.TIME_LIMIT_SECONDS,
            )
        else:
            p = run(
                cmd,
                input=input,
                stdout=stdout,
                encoding="utf8",
                errors="ignore",
                timeout=self.TIME_LIMIT_SECONDS,
            )
        assert p.returncode == 0, f"código de saída é {p.returncode}"
        return p

    def run_binary(
        self,
        cmd,
        stdin,
        stdout,
        input=None,
        in_filename=None,
        out_filename=None,
    ):
        cmd_str = " ".join([c if " " not in c and c != "" else f'"{c}"' for c in cmd])
        if in_filename:
            cmd_str += f" < {in_filename}"
        if out_filename:
            cmd_str += f" > {out_filename}"
        if input:
            cmd_str += f' com entrada "{input}"'
        try:
            return self.run_binary_inner(cmd, stdin, stdout, input)
        except AssertionError as e:
            raise AssertionError(f"falha ao executar {cmd_str} : {e}")
        except TimeoutExpired:
            raise AssertionError(f"falha ao executar {cmd_str} : tempo limite de {self.TIME_LIMIT_SECONDS}s excedido")

    def test_one_case(self, cmd, in_filename):
        out_filename = in_filename.replace(".in", ".out")
        res_filename = in_filename.replace(".in", ".res")
        with open(in_filename) as i, open(out_filename, "w") as o:
            self.run_binary(cmd, i, o, in_filename=in_filename, out_filename=out_filename)
        ok = self.compare_files(out_filename, res_filename)
        assert ok, f'execute: diff "{out_filename}" "{res_filename}"'

    def test_cases(self, script, in_filenames, args=[]) -> None:
        self.exists(script)
        cmd = [self.python3, script] + args
        assert isinstance(in_filenames, list) and isinstance(in_filenames[0], str), (
            "erro no caso de teste, deveria ser lista de strings"
        )
        errors = []
        for in_filename in in_filenames:
            try:
                self.tested_cases.add(in_filename)
                self.test_one_case(cmd, in_filename)
                self.passed_cases.add(in_filename)
                print(f"  -> {in_filename} passou ✅")
            except AssertionError as e:
                print(f"  -> {in_filename} falhou ❌")
                errors.append(str(e))
                if not self.continue_on_error:
                    break
        assert not errors, "\n  -> ".join(errors)

    def input_output(self, script, input, expected, args=[]):
        self.exists(script)
        cmd = [self.python3, script] + args
        p = self.run_binary(cmd, None, PIPE, input=input)
        output = p.stdout.strip()
        ok = self.compare_output(output, expected)
        assert ok, f'para entrada "{input}", a saída é "{output}", mas era esperado "{expected}"'

    def should_test(self, name):
        if not name.startswith("teste_"):
            return False
        if not self.only_matching:
            return True
        for pattern in self.only_matching:
            if pattern in name:
                return True
        return False

    def test_units(self):
        for name in sorted(dir(self)):
            if not self.should_test(name):
                continue
            print()
            print(f"Executando {name}...")
            sys.stderr.flush()
            sys.stdout.flush()
            try:
                test = getattr(self, name)
                self.tested_units.add(name)
                test()
                self.passed_units.add(name)
                print(f"{name}: OK")
            except AssertionError as e:
                print(f"{name}: FALHOU")
                if "privado" not in name or self.show_all_errors:
                    print(f"  -> {e}\n")
                if not self.continue_on_error:
                    break

    def case_range(self, input_template, start, end, folder="testes"):
        input_files = []
        for i in range(start, end + 1):
            input_files.append(join(folder, input_template.format(i)))
        self.number_cases += len(input_files)
        return input_files

    def has_n_words(self, filename, n_words):
        text = self.read_file_utf8(filename)
        length = len(text.split())
        assert length >= n_words, f"{filename} deve ter pelos menos {n_words} palavras"

    @staticmethod
    @contextmanager
    def time_limit(seconds, desc):
        timer = threading.Timer(seconds, lambda: _thread.interrupt_main())
        timer.start()
        try:
            yield
        except KeyboardInterrupt:
            raise AssertionError(f"{desc} falhou: tempo limite de {seconds}s excedido")
        finally:
            timer.cancel()

    def test_closure(self, closure, desc="comando"):
        import traceback

        with self.time_limit(self.TIME_LIMIT_SECONDS, desc):
            try:
                closure()
            except Exception:
                tb = traceback.format_exc()
                assert False, f"algum erro ocorreu durante a execução:\n{tb}"


def compare_deep_dictionaries(dict1, dict2, path=""):
    """
    Compares two deeply nested dictionaries and prints differences.
    """
    if isinstance(dict1, dict) and isinstance(dict2, dict):
        keys1 = set(dict1.keys())
        keys2 = set(dict2.keys())
        for key in sorted(keys1.union(keys2), key=lambda x: 0 if x is None else x):
            new_path = f"{path}.{key}" if path else key
            if key not in dict1:
                return f"Chave '{new_path}' faltando na saída."
            elif key not in dict2:
                return f"Chave '{new_path}' na saída não esperada."
            else:
                error = compare_deep_dictionaries(dict1[key], dict2[key], new_path)
                if error is not None:
                    return error
    elif isinstance(dict1, list) and isinstance(dict2, list):
        if len(dict1) != len(dict2):
            return f"Lista '{path}' tem tamanho {len(dict1)}, mas era esperado {len(dict2)}."
        for i, (item1, item2) in enumerate(zip(dict1, dict2)):
            error = compare_deep_dictionaries(item1, item2, f"{path}[{i}]")
            if error is not None:
                return error
    elif dict1 != dict2:
        return f"Valor em '{path}' é {dict1}, mas era esperado {dict2}."
    return None


class Task(BaseTask):
    @staticmethod
    def get_json_path_list(in_filename):
        json_list = []
        with open(in_filename) as f:
            for line in f:
                if line.startswith("GRAVAR-ARQUIVO:"):
                    out_img = line.split(":")[1].strip()
                    res_img = out_img.replace(".out.json", ".res.json")
                    json_list.append((out_img, res_img))
        return json_list

    @staticmethod
    def read_json(json_path):
        import json

        try:
            with open(json_path) as f:
                return json.load(f)
        except:  # noqa
            raise AssertionError(f"Falha ao ler JSON {json_path}")

    def test_one_case(self, cmd, in_filename):
        super().test_one_case(cmd, in_filename)
        for out_json_path, res_json_path in self.get_json_path_list(in_filename):
            out_data = self.read_json(out_json_path)
            res_data = self.read_json(res_json_path)
            error = compare_deep_dictionaries(out_data, res_data, "dados_json_out")
            if error is not None:
                print(error)
                raise AssertionError(f'execute: diff "{out_json_path}" "{res_json_path}"')

    def teste_11_descrever(self):
        cases = self.case_range("descrever_colecao{}.in", 1, 7, folder="testes")
        script = "gerenciador.py"
        self.test_cases(script, cases)

    def teste_21_citacoes(self):
        cases = self.case_range("buscar_citacoes{}.in", 1, 5, folder="testes")
        script = "gerenciador.py"
        self.test_cases(script, cases)

    def teste_22_citacoes(self):
        cases = self.case_range("buscar_citacoes{}.in", 6, 6, folder="testes")
        script = "gerenciador.py"
        self.test_cases(script, cases)

    def teste_31_palavras(self):
        cases = self.case_range("buscar_palavras{}.in", 1, 6, folder="testes")
        script = "gerenciador.py"
        self.test_cases(script, cases)

    def teste_41_gerenciar(self):
        cases = self.case_range("gerenciar_artigos{}.in", 1, 6, folder="testes")
        script = "gerenciador.py"
        self.test_cases(script, cases)

    def teste_42_gerenciar(self):
        cases = self.case_range("busca_avancada_palavras{}.in", 1, 1, folder="testes")
        script = "gerenciador.py"
        self.test_cases(script, cases)

    def teste_43_gerenciar(self):
        self.TIME_LIMIT_SECONDS = 0.3
        cases = self.case_range("busca_avancada_citacoes{}.in", 1, 2, folder="testes")
        script = "gerenciador.py"
        self.test_cases(script, cases)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Testa tarefa.")
    parser.add_argument("only", nargs="*", help="apenas unidades contendo essa string")
    parser.add_argument("-c", action="store_true", help="continua mesmo que anteriores falhem")
    args = parser.parse_args()
    Task(args.c, args.only).test_units()
