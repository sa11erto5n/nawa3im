from django.conf import settings
import os
import polib
from django.core.management.base import BaseCommand
from googletrans import Translator

class Command(BaseCommand):
    """Django management command to translate .po files using Google Translate API.
    
    This command processes .po files in the configured LOCALE_PATHS, translating
    message strings from a source language to target languages using Google Translate.
    """
    
    help = 'Translate .po files using Google Translator'

    def add_arguments(self, parser):
        """Define command-line arguments for the translation process.
        
        Args:
            parser: ArgumentParser object to add arguments to
            
        Options:
            -u, --untranslated_only: Only translate untranslated strings
        """
        parser.add_argument('-u', '--untranslated_only', action='store_true', help='Translate only untranslated strings')

    def translate_text(self, text, source_lang, target_lang):
        """Translate text using Google Translate API.
        
        Args:
            text: The text to translate
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            str: Translated text or original text if translation fails
            
        Raises:
            Exception: If translation fails
        """
        if not text:
            return text
            
        translator = Translator()
        try:
            translation = translator.translate(text, src=source_lang, dest=target_lang)
            if translation and hasattr(translation, 'text'):
                return translation.text
            return text  # Return original text if translation fails
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Translation failed for '{text}': {str(e)}"))
            return text  # Return original text on error

    def handle(self, *args, **options):
        """Main command execution logic.
        
        Processes all .po files in LOCALE_PATHS, translating messages from the
        source language to all other available languages.
        
        Args:
            *args: Additional arguments
            **options: Command-line options
            
        Workflow:
            1. Validate LOCALE_PATHS configuration
            2. Iterate through each locale path
            3. Process each language directory
            4. Load and translate .po files
            5. Save translated .po files
            6. Compile to .mo files
        """
        source_lang = 'en'  # Always use English as source language
        untranslated_only = options['untranslated_only']
        
        if not settings.LOCALE_PATHS:
            self.stdout.write(self.style.ERROR('No LOCALE_PATHS configured in settings'))
            return

        # Iterate through all locale paths
        for locale_path in settings.LOCALE_PATHS:
            self.stdout.write(self.style.SUCCESS(f'Processing locale path: {locale_path}'))
            
            # Process each language directory in the locale path
            for lang_dir in os.listdir(locale_path):
                lang_path = os.path.join(locale_path, lang_dir)
                
                # Only process directories that represent languages
                if os.path.isdir(lang_path) and lang_dir != source_lang:
                    self.stdout.write(f'Processing language: {lang_dir}')
                    
                    # Find the .po file in LC_MESSAGES
                    po_file_path = os.path.join(lang_path, 'LC_MESSAGES', 'django.po')
                    
                    if os.path.exists(po_file_path):
                        try:
                            # Load the .po file
                            po_file = polib.pofile(po_file_path)
                            
                            # Translate all msgid entries
                            for entry in po_file:
                                if entry.msgid and (not entry.msgstr or not untranslated_only):
                                    try:
                                        entry.msgstr = self.translate_text(
                                            entry.msgid,
                                            source_lang,
                                            lang_dir
                                        )
                                        self.stdout.write(f'Translated: {entry.msgid} -> {entry.msgstr}')
                                    except Exception as e:
                                        self.stdout.write(self.style.ERROR(f"Error translating {entry.msgid}: {str(e)}"))
                                        continue
                            
                            # Save the translated .po file
                            po_file.save(po_file_path)
                            self.stdout.write(self.style.SUCCESS(f'Saved translations to {po_file_path}'))
                            
                            # Compile to .mo file
                            mo_file_path = po_file_path.replace('.po', '.mo')
                            po_file.save_as_mofile(mo_file_path)
                            self.stdout.write(self.style.SUCCESS(f'Compiled translations to {mo_file_path}'))
                            
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f"Error processing {lang_dir}: {str(e)}"))
                    else:
                        self.stdout.write(self.style.WARNING(f'No django.po file found in {lang_path}'))

