# -*- coding: utf-8 -*-
"""
Forms for import.
"""
import os

from django import forms


class ImportForm(forms.Form):
    """
    Form for import hydrants.
    """

    file = forms.FileField(
        widget=forms.FileInput(
            attrs={
                "id": "file",
                "class": "form-control",
                "accept": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            },
        ),
    )

    def clean_file(self):
        """
        Validate function for checking file size and file type.
        """
        file = self.cleaned_data["file"]
        extension = os.path.splitext(file.name)[1][1:].lower()
        if file.size > 104857600:
            raise forms.ValidationError(
                "Maximum file size up to 100MB",
            )
        if extension != "xlsx":
            raise forms.ValidationError("This file is not valid")
        return file
