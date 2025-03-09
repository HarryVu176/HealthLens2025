import sys
import json
import os
from imageToText import ImageToFacts
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
                             QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit,
                             QFrame, QFileDialog, QComboBox, QStackedWidget,
                             QSplitter, QSizePolicy, QToolBar, QScrollArea,
                             QGraphicsDropShadowEffect)
from PyQt6.QtGui import QPixmap, QImage, QFont, QIcon, QColor, QPalette, QFontDatabase
from PyQt6.QtCore import Qt, QTimer, QSize, QPropertyAnimation, QEasingCurve, QRect

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
import matplotlib.patches as patches
from PIL import Image, ImageQt

# Style Constants
MATERIAL_PRIMARY = "#2979FF"  # Blue primary
MATERIAL_PRIMARY_DARK = "#2962FF"  # Dark blue for hover
MATERIAL_SECONDARY = "#FF6D00"  # Orange accent
MATERIAL_BACKGROUND = "#FAFAFA"  # Light gray background
MATERIAL_CARD = "#FFFFFF"  # White card surface
MATERIAL_TEXT_PRIMARY = "#212121"  # Near black text
MATERIAL_TEXT_SECONDARY = "#757575"  # Medium gray text


# Mock GeminiClient for demonstration purposes
class GeminiClient:
    def analyze_prescription(self, image_path):
        # Mock response that would come from Gemini API
        imgToFact = ImageToFacts()
        image = Image.open(image_path)
        text = imgToFact.process(image)
        return text
        # return """
        # Medication: Lisinopril 10mg
        #
        # Instructions: Take one tablet by mouth once daily
        #
        # Prescribing Doctor: Dr. Smith
        #
        # Purpose: This medication is an ACE inhibitor used to treat high blood pressure and heart failure.
        #
        # Common Side Effects:
        # - Dizziness
        # - Cough
        # - Headache
        #
        # Take with or without food. Avoid potassium supplements.
        # """

    def simplify_medical_text(self, medical_text):
        # Mock response for text simplification
        return """
        The patient is having a heart attack, with specific changes seen on their heart test (ECG) in certain areas.

        Blood tests show proteins that indicate heart damage.

        The patient needs a procedure where a small tube (catheter) will be used to open the blocked blood vessel supplying the front of their heart.

        After the procedure, they will need to take two blood-thinning medications:
        - Aspirin (a baby aspirin) once per day
        - Clopidogrel (Plavix) once per day

        The medical team will watch for signs that the heart is not pumping effectively, including fluid in the lungs and reduced heart pumping strength.
        """

    def get_medication_effects(self, medication_name):
        # Mock response for medication effects
        return json.dumps({
            "primary_systems": ["cardiovascular", "renal"],
            "side_effects": {
                "brain": "May cause dizziness or headache",
                "lungs": "Can cause dry cough in some patients",
                "kidneys": "Changes kidney function to reduce blood pressure"
            },
            "mechanism": "Blocks an enzyme that produces a substance that narrows blood vessels."
        })


# Material Card - a container with shadow effect
class MaterialCard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("MaterialCard")

        # Set rounded corners and white background
        self.setStyleSheet("""
            #MaterialCard {
                background-color: #FFFFFF;
                border-radius: 8px;
                padding: 16px;
            }
        """)

        # Add shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 3)
        self.setGraphicsEffect(shadow)

        # Layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(16, 16, 16, 16)
        self.layout.setSpacing(12)


# Material Button
class MaterialButton(QPushButton):
    def __init__(self, text, icon=None, accent=False, parent=None):
        super().__init__(text, parent)
        self.setObjectName("MaterialButton")

        if icon:
            self.setIcon(icon)
            self.setIconSize(QSize(24, 24))

        # Style button based on type (primary or accent)
        color = MATERIAL_SECONDARY if accent else MATERIAL_PRIMARY
        hover_color = "#FF8F00" if accent else MATERIAL_PRIMARY_DARK
        text_color = "#FFFFFF"

        self.setStyleSheet(f"""
            #MaterialButton {{
                background-color: {color};
                color: {text_color};
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
                min-height: 36px;
            }}

            #MaterialButton:hover {{
                background-color: {hover_color};
            }}

            #MaterialButton:pressed {{
                background-color: {color};
            }}

            #MaterialButton:disabled {{
                background-color: #BDBDBD;
                color: #757575;
            }}
        """)


# Text Button (flat)
class TextButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setObjectName("TextButton")

        self.setStyleSheet("""
            #TextButton {
                background-color: transparent;
                color: #2979FF;
                border: none;
                padding: 8px 16px;
                text-align: center;
                font-weight: bold;
            }

            #TextButton:hover {
                background-color: rgba(41, 121, 255, 0.1);
            }

            #TextButton:pressed {
                background-color: rgba(41, 121, 255, 0.2);
            }
        """)


# MatplotlibCanvas for displaying the body visualization
class MatplotlibCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=8, dpi=100):
        plt.style.use('seaborn-v0_8-whitegrid')  # Modern clean style
        self.fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        self.fig.patch.set_facecolor('#FFFFFF')  # White background
        super(MatplotlibCanvas, self).__init__(self.fig)
        self.setParent(parent)

        # Using a better human body outline - stylized for material design
        body = patches.Rectangle((0.3, 0.1), 0.4, 0.8, fill=False,
                                 color='#424242', linewidth=3, linestyle='-')
        self.ax.add_patch(body)

        # Add better looking organs with subtle colors
        # Brain
        brain = patches.Circle((0.5, 0.9), 0.1, fill=True, alpha=0.5,
                               color='#90CAF9', linewidth=0, edgecolor='none')
        self.ax.add_patch(brain)
        self.ax.text(0.5, 0.9, "Brain", ha='center', va='center',
                     fontsize=10, fontweight='bold', color='#424242')

        # Heart
        heart = patches.Circle((0.5, 0.65), 0.08, fill=True, alpha=0.7,
                               color='#EF5350', linewidth=0)
        self.ax.add_patch(heart)
        self.ax.text(0.5, 0.65, "Heart", ha='center', va='center',
                     fontsize=10, fontweight='bold', color='#424242')

        # Lungs
        lungs_left = patches.Ellipse((0.4, 0.65), 0.1, 0.15, fill=True,
                                     alpha=0.6, color='#FFCC80', linewidth=0)
        lungs_right = patches.Ellipse((0.6, 0.65), 0.1, 0.15, fill=True,
                                      alpha=0.6, color='#FFCC80', linewidth=0)
        self.ax.add_patch(lungs_left)
        self.ax.add_patch(lungs_right)
        self.ax.text(0.4, 0.65, "Lung", ha='center', va='center',
                     fontsize=9, fontweight='bold', color='#424242')
        self.ax.text(0.6, 0.65, "Lung", ha='center', va='center',
                     fontsize=9, fontweight='bold', color='#424242')

        # Stomach
        stomach = patches.Ellipse((0.5, 0.5), 0.15, 0.1, fill=True,
                                  alpha=0.5, color='#81C784', linewidth=0)
        self.ax.add_patch(stomach)
        self.ax.text(0.5, 0.5, "Stomach", ha='center', va='center',
                     fontsize=10, fontweight='bold', color='#424242')

        # Liver
        liver = patches.Ellipse((0.4, 0.45), 0.1, 0.08, fill=True,
                                alpha=0.6, color='#A1887F', linewidth=0)
        self.ax.add_patch(liver)
        self.ax.text(0.4, 0.45, "Liver", ha='center', va='center',
                     fontsize=9, fontweight='bold', color='#424242')

        # Kidneys
        kidney_left = patches.Ellipse((0.4, 0.4), 0.08, 0.05, fill=True,
                                      alpha=0.7, color='#9575CD', linewidth=0)
        kidney_right = patches.Ellipse((0.6, 0.4), 0.08, 0.05, fill=True,
                                       alpha=0.7, color='#9575CD', linewidth=0)
        self.ax.add_patch(kidney_left)
        self.ax.add_patch(kidney_right)
        self.ax.text(0.5, 0.4, "Kidneys", ha='center', va='center',
                     fontsize=10, fontweight='bold', color='#424242')

        # Remove axes
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        self.ax.axis('off')


# Scanner Widget with Material Design
class ScannerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.gemini_client = GeminiClient()
        self.current_image_path = None
        self.current_medication = None
        self.initUI()

    def initUI(self):
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)

        # Title
        title_label = QLabel("Prescription Scanner")
        title_label.setFont(QFont('Segoe UI', 24, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {MATERIAL_TEXT_PRIMARY};")
        main_layout.addWidget(title_label)

        # Subtitle
        subtitle = QLabel("Scan your prescription to understand how it affects your body")
        subtitle.setFont(QFont('Segoe UI', 14))
        subtitle.setStyleSheet(f"color: {MATERIAL_TEXT_SECONDARY};")
        main_layout.addWidget(subtitle)

        # Content layout (two cards side by side)
        content_layout = QHBoxLayout()
        content_layout.setSpacing(24)

        # Left card - Image input
        left_card = MaterialCard()
        left_layout = left_card.layout

        image_label = QLabel("Prescription Image")
        image_label.setFont(QFont('Segoe UI', 14, QFont.Weight.Bold))
        left_layout.addWidget(image_label)

        self.image_display = QLabel("No image selected")
        self.image_display.setFixedSize(340, 240)
        self.image_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_display.setStyleSheet("""
            background-color: #E0E0E0;
            border-radius: 4px;
            color: #757575;
            font-size: 14px;
        """)
        left_layout.addWidget(self.image_display)

        # Buttons
        button_layout = QHBoxLayout()

        self.upload_button = MaterialButton("Upload Image")
        self.upload_button.clicked.connect(self.upload_image)
        button_layout.addWidget(self.upload_button)

        self.camera_button = MaterialButton("Take Photo", accent=True)
        self.camera_button.clicked.connect(self.take_photo)
        button_layout.addWidget(self.camera_button)

        left_layout.addLayout(button_layout)
        left_layout.addStretch()

        # Right card - Results
        right_card = MaterialCard()
        right_layout = right_card.layout

        results_label = QLabel("Analysis Results")
        results_label.setFont(QFont('Segoe UI', 14, QFont.Weight.Bold))
        right_layout.addWidget(results_label)

        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setMinimumHeight(200)
        self.results_text.setStyleSheet("""
            border: 1px solid #E0E0E0;
            border-radius: 4px;
            padding: 12px;
            background-color: #F5F5F5;
            color: #212121;
            font-family: 'Segoe UI';
            font-size: 14px;
        """)
        right_layout.addWidget(self.results_text)

        action_layout = QHBoxLayout()

        self.analyze_button = MaterialButton("Analyze Prescription")
        self.analyze_button.clicked.connect(self.analyze_prescription)
        action_layout.addWidget(self.analyze_button)

        self.view_effects_button = MaterialButton("View Body Effects", accent=True)
        self.view_effects_button.clicked.connect(self.view_body_effects)
        self.view_effects_button.setEnabled(False)
        action_layout.addWidget(self.view_effects_button)

        right_layout.addLayout(action_layout)

        # Add cards to content layout
        content_layout.addWidget(left_card, 1)
        content_layout.addWidget(right_card, 1)

        # Add content layout to main layout
        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

        # Set background color
        self.setStyleSheet(f"background-color: {MATERIAL_BACKGROUND};")

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg)"
        )

        if file_path:
            self.current_image_path = file_path
            self.display_image(file_path)

    def take_photo(self):
        # For a hackathon, this could be simulated with a pre-taken image
        self.results_text.append("Camera functionality would be implemented here.")

        # For demo purposes, use dummy data
        self.current_image_path = "dummy_path"

        # Create a blank image for demo
        image = QImage(340, 240, QImage.Format.Format_RGB32)
        image.fill(QColor('#2979FF'))
        pixmap = QPixmap.fromImage(image)
        self.image_display.setPixmap(pixmap)
        self.image_display.setText("")  # Clear text when showing image

    def display_image(self, image_path):
        try:
            pixmap = QPixmap(image_path)
            pixmap = pixmap.scaled(340, 240, Qt.AspectRatioMode.KeepAspectRatio)
            self.image_display.setPixmap(pixmap)
            self.image_display.setText("")  # Clear text when showing image
        except Exception as e:
            self.image_display.setText(f"Error loading image: {e}")

    def analyze_prescription(self):
        if not self.current_image_path:
            self.results_text.setText("Please upload or take a prescription image first.")
            return

        # For a hackathon, we can use a predefined response for demo purposes
        self.results_text.setText("Analyzing prescription...")

        # Simulate API call delay
        QTimer.singleShot(1000, self.display_analysis_results)

    def display_analysis_results(self):
        # Get mock analysis result
        analysis_result = self.gemini_client.analyze_prescription(self.current_image_path)

        self.results_text.setText(analysis_result)
        self.current_medication = "Lisinopril"
        self.view_effects_button.setEnabled(True)

    def view_body_effects(self):
        # Switch to body viewer with current medication
        if self.parent and hasattr(self.parent, 'set_current_medication'):
            self.parent.set_current_medication(self.current_medication)
            self.parent.switch_to_tab(1)  # Switch to body viewer tab


# Body Viewer Widget with Material Design
class BodyViewerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.medication_name = "Sample Medication"
        self.initUI()

    def set_medication(self, medication_name):
        self.medication_name = medication_name
        self.update_title()
        self.update_info()

    def update_title(self):
        self.title_label.setText(f"How {self.medication_name} Affects Your Body")

    def update_info(self):
        sample_info = f"""
        {self.medication_name} (ACE Inhibitor):

        Primary Effects:
        - Heart: Reduces blood pressure by relaxing blood vessels
        - Kidneys: Changes kidney function to reduce blood pressure

        Common Side Effects:
        - Brain: May cause dizziness or headache
        - Lungs: Can cause dry cough in some patients

        How it works: Blocks an enzyme that produces a substance that narrows blood vessels.
        """
        self.info_text.setText(sample_info)

    def initUI(self):
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)

        # Title
        self.title_label = QLabel(f"How {self.medication_name} Affects Your Body")
        self.title_label.setFont(QFont('Segoe UI', 24, QFont.Weight.Bold))
        self.title_label.setStyleSheet(f"color: {MATERIAL_TEXT_PRIMARY};")
        main_layout.addWidget(self.title_label)

        # Subtitle
        subtitle = QLabel("Interactive visualization of medication effects")
        subtitle.setFont(QFont('Segoe UI', 14))
        subtitle.setStyleSheet(f"color: {MATERIAL_TEXT_SECONDARY};")
        main_layout.addWidget(subtitle)

        # Content layout
        content_layout = QHBoxLayout()
        content_layout.setSpacing(24)

        # Left card - Body visualization
        vis_card = MaterialCard()
        vis_layout = vis_card.layout

        self.canvas = MatplotlibCanvas(vis_card)
        vis_layout.addWidget(self.canvas)

        # Right card - Information
        info_card = MaterialCard()
        info_layout = info_card.layout

        info_title = QLabel("Medication Information")
        info_title.setFont(QFont('Segoe UI', 14, QFont.Weight.Bold))
        info_layout.addWidget(info_title)

        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        self.info_text.setMinimumHeight(200)
        self.info_text.setStyleSheet("""
            border: 1px solid #E0E0E0;
            border-radius: 4px;
            padding: 12px;
            background-color: #F5F5F5;
            color: #212121;
            font-family: 'Segoe UI';
            font-size: 14px;
            line-height: 1.5;
        """)
        info_layout.addWidget(self.info_text)

        # Add cards to content layout
        content_layout.addWidget(vis_card, 1)
        content_layout.addWidget(info_card, 1)

        # Add content layout to main layout
        main_layout.addLayout(content_layout)

        # Back button
        back_button = TextButton("← Back to Prescription Scanner")
        back_button.clicked.connect(self.go_back)
        main_layout.addWidget(back_button, 0, Qt.AlignmentFlag.AlignLeft)

        self.setLayout(main_layout)

        # Set background color
        self.setStyleSheet(f"background-color: {MATERIAL_BACKGROUND};")

        # Populate with sample data
        self.update_info()

    def go_back(self):
        if self.parent:
            self.parent.switch_to_tab(0)  # Switch back to scanner tab


# Translator Widget with Material Design
class TranslatorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.gemini_client = GeminiClient()
        self.initUI()

    def initUI(self):
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)

        # Title
        title_label = QLabel("Medical Term Translator")
        title_label.setFont(QFont('Segoe UI', 24, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {MATERIAL_TEXT_PRIMARY};")
        main_layout.addWidget(title_label)

        # Subtitle
        subtitle = QLabel("Convert complex medical language into simple explanations")
        subtitle.setFont(QFont('Segoe UI', 14))
        subtitle.setStyleSheet(f"color: {MATERIAL_TEXT_SECONDARY};")
        main_layout.addWidget(subtitle)

        # Main content card
        content_card = MaterialCard()
        card_layout = content_card.layout

        # Input section
        input_label = QLabel("Enter Medical Text:")
        input_label.setFont(QFont('Segoe UI', 14, QFont.Weight.Bold))
        card_layout.addWidget(input_label)

        self.input_text = QTextEdit()
        self.input_text.setMinimumHeight(150)
        self.input_text.setStyleSheet("""
            border: 1px solid #E0E0E0;
            border-radius: 4px;
            padding: 12px;
            background-color: #F5F5F5;
            color: #212121;
            font-family: 'Segoe UI';
            font-size: 14px;
        """)
        card_layout.addWidget(self.input_text)

        # Controls layout
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(12)

        # Sample text button
        self.sample_button = TextButton("Use Sample Text")
        self.sample_button.clicked.connect(self.load_sample_text)
        controls_layout.addWidget(self.sample_button)

        # Spacer
        controls_layout.addStretch()

        # Language selector
        language_label = QLabel("Language:")
        language_label.setStyleSheet(f"color: {MATERIAL_TEXT_PRIMARY};")
        controls_layout.addWidget(language_label)

        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "Spanish", "French", "Chinese", "Arabic"])
        self.language_combo.setStyleSheet("""
            border: 1px solid #E0E0E0;
            border-radius: 4px;
            padding: 4px 12px;
            background-color: white;
            min-height: 32px;
        """)
        controls_layout.addWidget(self.language_combo)

        card_layout.addLayout(controls_layout)

        # Action buttons
        action_layout = QHBoxLayout()

        # Clear button
        self.clear_button = TextButton("Clear All")
        self.clear_button.clicked.connect(self.clear_all)
        action_layout.addWidget(self.clear_button)

        # Spacer
        action_layout.addStretch()

        # Translate button
        self.translate_button = MaterialButton("Simplify Language", accent=True)
        self.translate_button.clicked.connect(self.translate_text)
        action_layout.addWidget(self.translate_button)

        card_layout.addLayout(action_layout)

        # Results section
        results_label = QLabel("Simplified Text:")
        results_label.setFont(QFont('Segoe UI', 14, QFont.Weight.Bold))
        card_layout.addWidget(results_label)

        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setMinimumHeight(200)
        self.results_text.setStyleSheet("""
            border: 1px solid #E0E0E0;
            border-radius: 4px;
            padding: 12px;
            background-color: #F5F5F5;
            color: #212121;
            font-family: 'Segoe UI';
            font-size: 14px;
            line-height: 1.5;
        """)
        card_layout.addWidget(self.results_text)

        # Add card to main layout
        main_layout.addWidget(content_card)

        self.setLayout(main_layout)

        # Set background color
        self.setStyleSheet(f"background-color: {MATERIAL_BACKGROUND};")

    def load_sample_text(self):
        sample_text = """
        The patient presents with acute myocardial infarction with elevated ST segments in leads V1-V4. 
        Cardiac enzymes show troponin elevation of 0.8 ng/mL. 
        The patient will require percutaneous coronary intervention for revascularization of the occluded left anterior descending artery.
        Post-procedure, initiate dual antiplatelet therapy with aspirin 81mg daily and clopidogrel 75mg daily.
        Monitor for signs of heart failure including pulmonary edema and decreased ejection fraction.
        """

        self.input_text.setText(sample_text)

    def translate_text(self):
        medical_text = self.input_text.toPlainText().strip()

        if not medical_text:
            self.results_text.setText("Please enter some medical text to simplify.")
            return

        language = self.language_combo.currentText()

        # For hackathon demo
        self.results_text.setText("Simplifying text...")

        # Simulate API call delay
        QTimer.singleShot(1000, self.display_simplified_text)

    def display_simplified_text(self):
        # Get mock simplification
        simplified_text = self.gemini_client.simplify_medical_text("")

        self.results_text.setText(simplified_text)

    def clear_all(self):
        self.input_text.clear()
        self.results_text.clear()


# Main Application Window with Material Design
class MedicalSimplifierApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_medication = None
        self.initUI()

    def set_current_medication(self, medication):
        self.current_medication = medication
        # Update body viewer if it exists
        body_viewer = self.tab_widget.widget(1)
        if isinstance(body_viewer, BodyViewerWidget):
            body_viewer.set_medication(medication)

    def switch_to_tab(self, index):
        self.tab_widget.setCurrentIndex(index)

    def initUI(self):
        self.setWindowTitle("Medical Language Simplifier")
        self.setGeometry(100, 100, 1200, 800)

        # Set app-wide font
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif;
            }
        """)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create a toolbar for app navigation
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        toolbar.setStyleSheet(f"""
            QToolBar {{
                background-color: {MATERIAL_PRIMARY};
                spacing: 10px;
                padding: 8px 16px;
                border: none;
            }}
        """)

        # App title in toolbar
        app_title = QLabel("MedSimplify")
        app_title.setFont(QFont('Segoe UI', 18, QFont.Weight.Bold))
        app_title.setStyleSheet("color: white; padding: 0 16px;")
        toolbar.addWidget(app_title)

        # Add spacer
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        toolbar.addWidget(spacer)

        # Tab buttons in toolbar
        self.scanner_action = toolbar.addAction("Prescription Scanner")
        self.scanner_action.triggered.connect(lambda: self.switch_to_tab(0))

        self.body_action = toolbar.addAction("Body Visualizer")
        self.body_action.triggered.connect(lambda: self.switch_to_tab(1))

        self.translator_action = toolbar.addAction("Medical Translator")
        self.translator_action.triggered.connect(lambda: self.switch_to_tab(2))

        # Style the toolbar actions
        for action in toolbar.actions():
            widget = toolbar.widgetForAction(action)
            if widget:
                widget.setStyleSheet("""
                    color: white;
                    background-color: transparent;
                    padding: 8px 16px;
                    font-size: 14px;
                    border-radius: 4px;
                """)

        self.addToolBar(toolbar)

        # Tab widget for content
        self.tab_widget = QStackedWidget()

        # Add tabs
        self.scanner_widget = ScannerWidget(self)
        self.body_viewer_widget = BodyViewerWidget(self)
        self.translator_widget = TranslatorWidget(self)

        self.tab_widget.addWidget(self.scanner_widget)
        self.tab_widget.addWidget(self.body_viewer_widget)
        self.tab_widget.addWidget(self.translator_widget)

        main_layout.addWidget(self.tab_widget)

        # Status bar
        self.statusBar().showMessage('Ready')
        self.statusBar().setStyleSheet("""
            QStatusBar {
                background-color: #FAFAFA;
                color: #757575;
                border-top: 1px solid #E0E0E0;
                padding: 4px 16px;
            }
        """)


# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Enable high DPI scaling
    # app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    # app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)

    # Set application-wide palette
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(MATERIAL_BACKGROUND))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(MATERIAL_TEXT_PRIMARY))
    palette.setColor(QPalette.ColorRole.Base, QColor(MATERIAL_CARD))
    palette.setColor(QPalette.ColorRole.Text, QColor(MATERIAL_TEXT_PRIMARY))
    palette.setColor(QPalette.ColorRole.Button, QColor(MATERIAL_PRIMARY))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor('white'))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(MATERIAL_PRIMARY))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor('white'))
    app.setPalette(palette)

    window = MedicalSimplifierApp()
    window.show()
    sys.exit(app.exec())
