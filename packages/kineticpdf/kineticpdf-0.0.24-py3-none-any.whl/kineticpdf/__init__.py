#
# Kinetic PDF - 2023
#    Updates and wrapper around PDF handling functions updated for 2023.
#    Copyright 2023 - Kinetic Seas Inc, Chicago Illinois
#    Edward Honour, Joseph Lehman
#
#    Includes functions from pdfrw (https://github.com/pmaupin/pdfrw)
#           Copyright (C) 2006-2015 Patrick Maupin, Austin, Texas
#           MIT license -- See LICENSE.txt for details
#           pdfrw functions were the best for reading and writing Forms in PDF.
#
#           pdfrw has not been updated in years, so we included the
#           functions to make whatever changes necessary.
#
#    Includes functions from PyPDF2
#    PyPDF2 functions were the best for reading text from PDFs and
#           checking if a PDF is encrypyted.
#
#           PyPDF2 is deprecated, so we included the functions to make
#           whatever changes necessary.
#
#           Documentation: <URL coming soon>
#           FAQ: <http://mstamy2.github.io/PyPDF2/FAQ.html>
#           PyPI: <https://pypi.python.org/pypi/PyPDF2>
#           GitHub: <https://github.com/mstamy2/PyPDF2>
#           Homepage: <http://mstamy2.github.io/PyPDF2/>
#
#    PikePDF is a dependency and used to decrypt PDFs.
#           pikepdf is a Python library for reading and writing PDF files.
#
#           PikePDF is actively maintained so we DID not include thier
#           functions in this library.

from .pypdf2 import *                                       # Import PyPDF2 Functions.
from .pdf2 import generic
from .pdfwriter import PdfWriter                            # Import pdfrw implementation of PdfWriter.
from .pdfreader import PdfReader                            # Import pdfrw implementation of PdfReader.
from .objects import (PdfObject, PdfName, PdfArray,
                      PdfDict, IndirectPdfDict, PdfString)
from .tokens import PdfTokens
from .errors import PdfParseError
from .pagemerge import PageMerge
import os
import copy
import base64
import pikepdf

__version__ = '0.4'

# Add a tiny bit of compatibility to pyPdf

PdfFileReader = PdfReader
PdfFileWriter = PdfWriter

__all__ = """PdfWriter PdfReader PdfObject PdfName PdfArray
             PdfTokens PdfParseError PdfDict IndirectPdfDict
             PdfString PageMerge""".split()


class KineticPdf:

    def __init__(self):
        pass

        # Radio Buttons are always an issue.

    @staticmethod
    def is_pdf(filename):
        try:
            with open(filename, 'rb') as file:
                header = file.read(5)
                return header == b'%PDF-'
        except Exception as e:
            return False

    @staticmethod
    def set_radio_button_value(annotation, parent, desired_value):
        if annotation.get('/Parent') == parent:
            if '/' in desired_value:
                d = desired_value[1:]
            else:
                d = desired_value

            # parent.update(
            #     PdfDict(V='{}'.format(d))
            # )
            #### parent.update(PdfDict(V=PdfName(d)))
            if annotation['/AP']['/D']:
                if desired_value in annotation['/AP']['/D']:
                    pass
                    # This code is required to see changes in broswers
                    # but it is very scketchy when it comes to Acrobat Pro
                    annotation.update(PdfDict(AS=PdfName(d)))
                else:
                    # This code is required to see changes in broswers
                    # but it is very scketchy when it comes to Acrobat Pro
                    annotation.update(PdfDict(AS=PdfName('Off')))
                    pass

    #
    # fill_pdf_form: reads a PDF from the filesystem, applies new values,
    #                and writes output file.
    #
    @staticmethod
    def fill_pdf_form(input_pdf_path, output_pdf_path, new_values, hint=None):

        field_update_count = 0
        fields_updated = []

        # EH: new_values must be a dict or return error.
        if isinstance(new_values, dict):
            fields_missing = copy.deepcopy(new_values)
        else:
            error_code = "8001"
            error_msg = "New Values must be a dictionary."
            return {"error_code": error_code, "error_msg": error_msg, "data": {}}

        # EH: Output path must not be blank.
        if output_pdf_path == "":
            error_code = "8002"
            error_msg = "Output file path must not be blank."
            return {"error_code": error_code, "error_msg": error_msg, "data": {}}
        else:
            output_dir = os.path.dirname(output_pdf_path)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)

        # EH: Input path must not be blank.
        if input_pdf_path == "":
            error_code = "8002"
            error_msg = "Input PDF Path must not be blank."
            return {"error_code": error_code, "error_msg": error_msg, "data": {}}
        else:
            # Test input file exists.
            if os.path.exists(input_pdf_path):
                # Test if file is encrypted
                if KineticPdf.is_pdf_encrypted(input_pdf_path):
                    error_code = "8005"
                    error_msg = "Cannot fill a password protected PDF: " + str(input_pdf_path)
                    return {"error_code": error_code, "error_msg": error_msg, "data": {}}

                try:
                    # Attempt the read.
                    reader = PdfReader(input_pdf_path)
                except:
                    error_code = "8003"
                    error_msg = "Error Opening File: " + str(input_pdf_path)
                    return {"error_code": error_code, "error_msg": error_msg, "data": {}}

            else:
                error_code = "8003"
                error_msg = "Input file path does not exist: " + str(input_pdf_path)
                return {"error_code": error_code, "error_msg": error_msg, "data": {}}

        #
        # EH: If you don't set NeedsAppearances, updated forms may not appear
        # on different viewers, like Adobe Acrobat Pro.
        #
        if '/AcroForm' in reader.Root:
            pass
            reader.Root.AcroForm.update(PdfDict(NeedAppearances=PdfObject('true')))
        else:
            error_code = "8000"
            error_msg = "No Form in this PDF"
            return {"error_code": error_code, "error_msg": error_msg, "data": {}}

        #
        # EH: Iterate through each page and update form fields.  There are different
        # ways to process pages and annotations, but this seems to be the cleanest and
        # most stable.
        #
        for page in reader.pages:
            annotations = page['/Annots']
            if annotations:
                for annotation in annotations:

                    if annotation['/Subtype'] == '/Widget':
                        for key in new_values:

                            if annotation['/T']:
                                # textbox
                                # checkbox
                                # dropdown list
                                # listbox
                                # date field
                                field_name = annotation['/T'][1:-1]  # Remove parentheses around field name
                                if field_name == key:
                                    new_value = new_values[key]

                                    # EH: Checkboxes not set correctly.
                                    if new_value == '/Off':
                                        new_value = 'Off'
                                    if new_value == '/Yes':
                                        new_value = 'Yes'

                                    field_update_count += 1
                                    f = {key: new_values[key], "type": "annotation"}
                                    fields_updated.append(f)
                                    tmp = copy.deepcopy(fields_missing)
                                    if key in tmp:
                                        del fields_missing[key]

                                    if annotation['/FT'] == '/Btn' and '/AS' in annotation:
                                        # checkbox
                                        pass
                                        annotation.update(PdfDict(V=PdfName(new_value)))
                                        annotation.update(PdfDict(AS=PdfName(new_value)))
                                    elif annotation['/FT'] == '/Ch':
                                        # listbox
                                        # dropdown lists
                                        # currently do not work in Acrobat Pro
                                        # This is a problem area.
                                        ######################################################
                                        new_value2 = copy.deepcopy(new_value)
                                        annotation.update(PdfDict(V=new_value))
                                        annotation.update(PdfDict(AS=PdfName(new_value)))
                                        ######################################################
                                    else:
                                        pass
                                        # text fields
                                        # date fields
                                        #### annotation.update(PdfDict(AP=''))
                                        #### annotation.update(PdfDict(AS=PdfName(new_value)))
                                        #### annotation.update(PdfDict(V=new_value))
                            else:
                                #
                                # Type of Widget that is based on the parent (i.e) radio group/button
                                #

                                if annotation['/Parent']:
                                    parent = annotation['/Parent']
                                    if isinstance(parent, PdfDict) and '/T' in parent:
                                        my_name = parent['/T'][1:-1]
                                        if my_name == key:
                                            field_update_count += 1
                                            tmp = copy.deepcopy(fields_missing)
                                            if key in tmp:
                                               del fields_missing[key]

                                            new_value = new_values[key]
                                            KineticPdf.set_radio_button_value(annotation, annotation['/Parent'], new_value)
                                            f = {key: new_values[key], "type": "parent"}
                                            fields_updated.append(f)

        PdfWriter().write(output_pdf_path, reader)

        data = {"output_file_name": output_pdf_path, "field_count": str(field_update_count), "fields_updated": fields_updated, "fields_not_updated": fields_missing}
        output = {"error_code": "0", "error_msg": "", "data": data}

        return output

    @staticmethod
    def export_pdf_form(input_pdf_path, hint=None):
        if hint is not None:
            if isinstance(hint, dict):
                pass
            else:
                hint = {}

        i = KineticPdf.get_pdf_form(input_pdf_path, hint)
        data = i['data']
        for key in data:
            if data[key] is None:
                data[key] = ""
            elif data[key] == '/Off':
                data[key] = "off"
            elif data[key] == '/Yes':
                data[key] = 'on'

        i['data'] = data
        return i

    @staticmethod
    def import_pdf_form(data, hint=None):
        if hint is not None:
            if isinstance(hint, dict):
                use_hints = True
            else:
                hint = {}
                use_hints = False
        else:
            hint = {}
            use_hints = False

        for key in data:
            if data[key] == "":
                if use_hints:
                    for h in hint:
                        if h == key:
                            if hint[key] == "checkbox":
                                data[key] = "/Off"
                else:
                    pass

            if data[key] == "off":
                if use_hints:
                    for h in hint:
                        if h == key:
                            if hint[key] == "checkbox":
                                data[key] = "/Off"
                else:
                    data[key] = "/Off"

            if data[key] == "on":
                if use_hints:
                    for h in hint:
                        if h == key:
                            if hint[key] == "checkbox":
                                data[key] = "/On"
                else:
                    data[key] = "/Yes"
        return data

    @staticmethod
    def get_pdf_form(input_pdf_path, hint=None):

        # A hint is a dictionary object identifying the datatypes of the
        # fields in the form.  This is necessary because checkboxes will
        # return None if it has never been checked, /Off if it was once
        # checked by not now, and /Yes if it is currently checked.
        # {
        #    "first_name": "text",
        #    "salutation": "dropdown",
        #    "grade": "radio group",
        #    "enrolled": "checkbox",
        #    "todays_date": "date",
        #    "cats_name": "listbox" }

        if hint is not None:
            if isinstance(hint, dict):
                pass
            else:
                hint = {}

        # EH: Input path must not be blank.
        if input_pdf_path == "":
            error_code = "8002"
            error_msg = "Input PDF Path must not be blank."
            return {"error_code": error_code, "error_msg": error_msg, "data": {}}
        else:
            # Test input file exists.
            if os.path.exists(input_pdf_path):
                # Text that file is a PDF
                if not KineticPdf.is_pdf(input_pdf_path):
                    error_code = "8009"
                    error_msg = "File is not a valid PDF: " + str(input_pdf_path)
                    return {"error_code": error_code, "error_msg": error_msg, "data": {}}


                # Test if file is encrypted
                if KineticPdf.is_pdf_encrypted(input_pdf_path):
                    error_code = "8004"
                    error_msg = "Cannot read a password protected PDF: " + str(input_pdf_path)
                    return {"error_code": error_code, "error_msg": error_msg, "data": {}}

                try:
                    # Attempt the read.
                    annotations = PdfReader(input_pdf_path).Root.AcroForm.Fields
                except:
                    error_code = "8003"
                    error_msg = "Error Opening File: " + str(input_pdf_path)
                    return {"error_code": error_code, "error_msg": error_msg, "data": {}}
            else:
                error_code = "8003"
                error_msg = "Input file path does not exist: " + str(input_pdf_path)
                return {"error_code": error_code, "error_msg": error_msg, "data": {}}

        form_fields = {}
        for annotation in annotations:
            if annotation.FT == '/Tx':  # Field Type is Text
                key = annotation.T[1:-1]  # Remove parentheses around the key
                value = annotation.V[1:-1] if annotation.V else None
                if value is None:
                    for k in hint:
                        if hint[k]=="checkbox":
                            value="/Off"

                form_fields[key] = value
            elif annotation.FT == '/Btn':  # Field Type is Button (Checkboxes and Radio buttons)
                key = annotation.T[1:-1]
                value = annotation.V
                if value is None:
                    if hint is not None:
                        for k in hint:
                            if hint[k]=="checkbox":
                                value="/Off"
                            else:
                                value=""
                    else:
                        value=""
                form_fields[key] = value
            elif annotation.FT == '/Ch':
                key = annotation.T[1:-1]
                value = annotation.V
                if '(' in value:
                    value = value[1:-1]
                form_fields[key] = value

            # Add more field types (like /Ch for choice fields) as needed

        output = {"error_code": "0", "error_msg": "", "data": form_fields}
        return output

    @staticmethod
    def get_pdf_metadata(input_pdf_path, clean=True):

        # EH: Input path must not be blank.
        if input_pdf_path == "":
            error_code = "8002"
            error_msg = "Input PDF Path must not be blank."
            return {"error_code": error_code, "error_msg": error_msg, "data": {}}
        else:
            # Test input file exists.
            if os.path.exists(input_pdf_path):

                # Test if file is encrypted
                if KineticPdf.is_pdf_encrypted(input_pdf_path):
                    error_code = "8004"
                    error_msg = "Cannot read a password protected PDF: " + str(input_pdf_path)
                    return {"error_code": error_code, "error_msg": error_msg, "data": {}}

                try:
                    # Attempt the read.
                    pdf = PdfReader(input_pdf_path)
                except:
                    error_code = "8003"
                    error_msg = "Error Opening File: " + str(input_pdf_path)
                    return {"error_code": error_code, "error_msg": error_msg, "data": {}}
            else:
                error_code = "8003"
                error_msg = "Input file path does not exist: " + str(input_pdf_path)
                return {"error_code": error_code, "error_msg": error_msg, "data": {}}

        metadata = {}
        info = pdf.Info
        if info:
            for key in info.keys():
                if clean:
                    cleaned_key = key[1:]  # Remove '/' from the key
                else:
                    cleaned_key = key

                value = info[key]
                if value:
                    # Remove starting and ending parentheses if present
                    if value.startswith('(') and value.endswith(')'):
                        value = value[1:-1]
                    # Process keywords
                    if cleaned_key == "Keywords":
                        metadata[cleaned_key] = [keyword.strip() for keyword in value.split(",")]
                    else:
                        metadata[cleaned_key] = value
                else:
                    metadata[cleaned_key] = None

            # if 'Keywords' in metadata:
            #    keywords_list = metadata['Keywords']

            #    keywords_dict = {}
            #    for keyword in keywords_list:
            #        key, value = keyword.split('=')
            #        keywords_dict[key] = value

            #    metadata['keys'] = keywords_dict

        output = {"error_code": "0", "error_msg": "", "data": metadata}
        return output

    @staticmethod
    def get_pdf_text(input_pdf_path):
        # return {"error_code": "10", "error_msg": "", "data": {}}
        # EH: Input path must not be blank.
        if input_pdf_path == "":
            error_code = "8002"
            error_msg = "Input PDF Path must not be blank."
            return {"error_code": error_code, "error_msg": error_msg, "data": []}
        else:
            # Test input file exists.
            if os.path.exists(input_pdf_path):

                # Test if file is encrypted
                if KineticPdf.is_pdf_encrypted(input_pdf_path):
                    error_code = "8004"
                    error_msg = "Cannot read a password protected PDF: " + str(input_pdf_path)
                    return {"error_code": error_code, "error_msg": error_msg, "data": []}

                try:
                    # Attempt the read.
                    with open(input_pdf_path, 'rb') as file:
                        results = []
                        r = pypdf2.PdfReader(file)
                        for i in range(0, len(r.pages)):
                            text = r.pages[i].extract_text()
                            results.append(text)
                except:
                    error_code = "8003"
                    error_msg = "Error Opening File: " + str(input_pdf_path)
                    return {"error_code": error_code, "error_msg": error_msg, "data": []}
            else:
                error_code = "8003"
                error_msg = "Input file path does not exist: " + str(input_pdf_path)
                return {"error_code": error_code, "error_msg": error_msg, "data": []}

        output = {"error_code": "0", "error_msg": "", "data": results}
        print(output)
        return output

    @staticmethod
    def is_pdf_encrypted(pdf_path):
        with open(pdf_path, 'rb') as file:
            pdf_reader = pypdf2.PdfReader(file)
            return pdf_reader.is_encrypted

    @staticmethod
    def convert_to_base64(binary_data):
        if isinstance(binary_data, bytes) or isinstance(binary_data, bytearray):
            return base64.b64encode(binary_data).decode('utf-8')
        return binary_data

    @staticmethod
    def read_pdf_signature(input_pdf_path):

        # EH: Input path must not be blank.
        signatures = []

        if input_pdf_path == "":
            error_code = "8002"
            error_msg = "Input PDF Path must not be blank."
            return {"error_code": error_code, "error_msg": error_msg, "data": {}}
        else:
            # Test input file exists.
            if os.path.exists(input_pdf_path):

                # Test if file is encrypted
                if KineticPdf.is_pdf_encrypted(input_pdf_path):
                    error_code = "8004"
                    error_msg = "Cannot read a password protected PDF: " + str(input_pdf_path)
                    return {"error_code": error_code, "error_msg": error_msg, "data": {}}

                # Open the PDF
                with open(input_pdf_path, 'rb') as file:
                    pdf_reader = pypdf2.PdfReader(file)

                    for i in range(0, len(pdf_reader.pages)):
                        page = pdf_reader._get_page(i)
                        try:
                            annotations = page['/Annots']
                            for annotation in annotations:
                                obj = annotation.get_object()
                                if '/Subtype' in obj and obj['/Subtype'] == '/Widget' and '/AP' in obj and '/V' in obj:
                                    ap = obj['/V']
                                    r = ap.get_object()
                                    if isinstance(r, pdf2.generic.DictionaryObject):
                                        keys = list(r.keys())
                                        if '/Type' in r:
                                            if r['/Type'] in ['/Signature', '/Signature2', '/Sig']:
                                                processed_annotation = {k: KineticPdf.convert_to_base64(v) for k, v in r.items()}
                                                signatures.append(processed_annotation)
                        except KeyError:
                            pass  # No annotations on this page

        output = {"error_code": "0", "error_msg": "", "data": signatures}
        return output

    @staticmethod
    def process_pdf_file(j, func = None):
        #
        # EH: Open a PDF, grab the text, metadata, forms,
        # and signature and call a function.
        #

        if not isinstance(j, dict):
            return {"error_code": "4000", "error_msg": "Process_pdf: first parameter must be a dictionary"}

        if 'input_path' not in j:
            return {"error_code": "4001", "error_msg": "Process_pdf: first parameter must include input_path"}

        input_pdf_path = j['input_path']

        print(input_pdf_path)
        t = KineticPdf.get_pdf_text(input_pdf_path)
        if t['error_code'] == "0":
            pass
        else:
            return t

        info = KineticPdf.get_pdf_metadata(input_pdf_path, True)
        if info['error_code'] == "0":
            pass
        else:
            return info

        form = KineticPdf.get_pdf_form(input_pdf_path)
        if form['error_code'] == "0":
            pass
        else:
            return form

        sigs = KineticPdf.read_pdf_signature(input_pdf_path)
        if sigs['error_code'] == "0":
            pass
        else:
            return sigs

        if isinstance(info['data'], dict):
            pass
        else:
            info['data'] = {}

        if isinstance(info['data'], dict):
            pass
        else:
            info['data'] = {}

        if isinstance(t['data'], list):
            pass
        else:
            t['data'] = []

        if func is not None:
            output = func(info['data'], form['data'], t['data'], sigs['data'])
        else:
            output = {
                "pdf_file_path": input_pdf_path,
                "info": info['data'],
                "form": form['data'],
                "text": t['data'],
                "sigs": sigs['data']
            }
        return output


    @staticmethod
    def process_pdf_form(j, func=None):
        #
        # EH: Open a PDF, grab the text, metadata, forms,
        # and signature and call a function.
        #

        if not isinstance(j, dict):
            return {"error_code": "4000", "error_msg": "Process_pdf: first parameter must be a dictionary"}

        if 'input_path' not in j:
            return {"error_code": "4001", "error_msg": "Process_pdf: first parameter must include input_path"}

        input_pdf_path = j['input_path']

        info = KineticPdf.get_pdf_metadata(input_pdf_path, True)
        if info['error_code'] == "0":
            pass
        else:
            return info

        form = KineticPdf.get_pdf_form(input_pdf_path)
        if form['error_code'] == "0":
            pass
        else:
            return form

        sigs = KineticPdf.read_pdf_signature(input_pdf_path)
        if sigs['error_code'] == "0":
            pass
        else:
            return sigs

        if isinstance(info['data'], dict):
            pass
        else:
            info['data'] = {}

        if isinstance(info['data'], dict):
            pass
        else:
            info['data'] = {}

        if func is not None:
            jj = {
                "pdf_file_path": input_pdf_path,
                "info": info['data'],
                "form": form['data'],
                "sigs": sigs['data'],
            }
            output = func(jj)
        else:
            output = {
                "pdf_file_path": input_pdf_path,
                "info": info['data'],
                "form": form['data'],
                "sigs": sigs['data']
            }
        return output


    @staticmethod
    def decrypt_pdf(input_pdf_path, output_pdf_path, pwd):

        if output_pdf_path == "":
            error_code = "8002"
            error_msg = "Output file path must not be blank."
            return {"error_code": error_code, "error_msg": error_msg, "data": {}}
        else:
            output_dir = os.path.dirname(output_pdf_path)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)

        # EH: Input path must not be blank.
        if input_pdf_path == "":
            error_code = "8002"
            error_msg = "Input PDF Path must not be blank."
            return {"error_code": error_code, "error_msg": error_msg, "data": {}}
        else:
            # Test input file exists.
            if os.path.exists(input_pdf_path):
                # Test if file is encrypted
                if KineticPdf.is_pdf_encrypted(input_pdf_path):
                    with pikepdf.Pdf.open(input_pdf_path, password=pwd) as pdf:
                        try:
                            pdf.save(output_pdf_path)
                        except Exception as e:
                            return {"error_code": "8601", "error_msg": "An error occurred trying to decrypt: " + str(e),
                                    "data": {}}
                else:
                    error_code = "8009"
                    error_msg = "Trying to decrypt a file not encrypted: " + str(input_pdf_path)
                    return {"error_code": error_code, "error_msg": error_msg, "data": {}}

