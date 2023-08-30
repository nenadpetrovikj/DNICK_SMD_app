from django import forms

from .models import Category, Product


class AddProductForm(forms.ModelForm):

    category = forms.ModelChoiceField(label='Category', help_text='Required', queryset=Category.objects.all(), empty_label=None,
                                      widget=forms.Select(attrs={'class': 'form-select form-control'}))
    title = forms.CharField(label='Title', help_text='Required', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}))
    description = forms.CharField(label='Description', help_text='Optional', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product description'}))
    manufacturer = forms.CharField(label='Manufacturer', help_text='Required', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter manufacturer'}))
    memory = forms.IntegerField(label='Memory', help_text='Required', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter RAM size'}))
    storage = forms.IntegerField(label='Storage', help_text='Required', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter storage size'}))
    screen = forms.CharField(label='Screen', help_text='Required', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter screen specifications'}))
    processor = forms.CharField(label='Processor', help_text='Required', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter processor type'}))
    os = forms.CharField(label='Operating System', help_text='Required', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter operating system'}))
    battery = forms.IntegerField(label='Battery', help_text='Required', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter battery size'}))
    image = forms.ImageField(label='Image', help_text='Required', widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    slug = forms.SlugField(label='Slug', help_text='Required', widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.DecimalField(label='Price', help_text='Required', max_digits=8, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    in_stock = forms.BooleanField(label='Is the product in stock?', widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    is_active = forms.BooleanField(label='Should the product be seen by customers?', widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    class Meta:
        model = Product
        fields = ('category', 'title', 'manufacturer', 'memory', 'storage', 'screen', 'processor', 'os', 'battery', 'description', 'image', 'slug', 'price', 'in_stock', 'is_active')

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if Product.objects.filter(slug=slug).exists():
            raise forms.ValidationError("This slug is already in use. Please provide a unique slug.")
        return slug