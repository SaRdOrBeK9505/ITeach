from drf_yasg.inspectors import SwaggerAutoSchema
from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, FormParser


class AutoMultipartSchema(SwaggerAutoSchema):
    """
    Swagger UI da rasm va fayllarni to'g'ridan-to'g'ri tanlab (file input)
    test qilish imkoniyatini ta'minlovchi avtomatik schema inspektori.
    Agar serializerda ImageField/FileField bo'lsa yoki view MultiPartParser
    ishlatsa, swagger consumes ni multipart/form-data ga o'tkazadi.
    """

    def get_consumes(self):
        consumes = super().get_consumes()
        if self.method in ["POST", "PUT", "PATCH"]:
            parser_classes = self.get_parser_classes()
            has_multipart_parser = any(
                issubclass(p, MultiPartParser)
                for p in parser_classes
                if isinstance(p, type)
            )

            try:
                serializer = self.get_request_serializer()
                if serializer and hasattr(serializer, "fields"):
                    has_file_field = any(
                        isinstance(f, (serializers.FileField, serializers.ImageField))
                        for f in serializer.fields.values()
                    )
                    if has_file_field or has_multipart_parser:
                        return ["multipart/form-data"]
            except Exception:
                if has_multipart_parser:
                    return ["multipart/form-data"]

        return consumes
