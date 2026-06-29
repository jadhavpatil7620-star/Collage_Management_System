from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('results', '0001_initial'),
    ]

    operations = [
        # SubjectMarks: update default passing_marks from 35 → 15, max_marks from 100 → 25
        migrations.AlterField(
            model_name='subjectmarks',
            name='passing_marks',
            field=models.DecimalField(max_digits=6, decimal_places=2, default=15),
        ),
        migrations.AlterField(
            model_name='subjectmarks',
            name='max_marks',
            field=models.DecimalField(max_digits=6, decimal_places=2, default=25),
        ),
        # PracticalMarks: change max_marks default 50 → 30, add passing_marks field
        migrations.AlterField(
            model_name='practicalmarks',
            name='max_marks',
            field=models.DecimalField(max_digits=5, decimal_places=2, default=30),
        ),
        migrations.AddField(
            model_name='practicalmarks',
            name='passing_marks',
            field=models.DecimalField(max_digits=5, decimal_places=2, default=30),
        ),
    ]
