from django import forms
from .models import Post, Country, Sector, FakeNewsTechnique, CounterDisinfoTechnique

class PostForm(forms.ModelForm):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label="-- Select a Country --")
    sector = forms.ModelChoiceField(queryset=Sector.objects.all(), empty_label="-- Select a Sector --")
    fake_news_technique = forms.ModelChoiceField(queryset=FakeNewsTechnique.objects.all(), empty_label="-- Select a Fake News Technique --")
    counter_fake_news_technique = forms.ModelChoiceField(queryset=CounterDisinfoTechnique.objects.all(), empty_label="-- Select a Counter Fake News Technique --")

    class Meta:
        model = Post
        fields = ['country', 'sector', 'fake_news_technique', 'counter_fake_news_technique', 'description', 'image']
