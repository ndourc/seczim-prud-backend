from django.test import TestCase
from django.contrib.auth.models import User
from apps.core.models import SMI
from .models import Case, CaseNote, Investigation, AdHocInspection, CaseAttachment, CaseTimeline

class CaseManagementModuleTestCase(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test SMI
        self.smi = SMI.objects.create(
            company_name='Test Company Ltd',
            license_number='TEST001',
            business_type='Financial Services'
        )
        
        # Create test case
        self.case = Case.objects.create(
            case_type='INVESTIGATION',
            title='Test Investigation Case',
            description='Test case description',
            smi=self.smi,
            assigned_to=self.user,
            status='OPEN',
            priority='MEDIUM'
        )

    def test_case_creation(self):
        """Test creating a case"""
        case = Case.objects.create(
            case_type='COMPLAINT',
            title='Test Complaint Case',
            description='Test complaint description',
            smi=self.smi,
            assigned_to=self.user,
            status='OPEN',
            priority='HIGH'
        )
        self.assertEqual(case.case_type, 'COMPLAINT')
        self.assertEqual(case.title, 'Test Complaint Case')
        self.assertEqual(case.priority, 'HIGH')
        self.assertIsNotNone(case.case_number)

    def test_case_note_creation(self):
        """Test creating a case note"""
        note = CaseNote.objects.create(
            case=self.case,
            author=self.user,
            note='Test case note content'
        )
        self.assertEqual(note.case, self.case)
        self.assertEqual(note.author, self.user)
        self.assertEqual(note.note, 'Test case note content')

    def test_investigation_creation(self):
        """Test creating an investigation"""
        investigation = Investigation.objects.create(
            case=self.case,
            investigation_type='REGULATORY',
            scope='Test investigation scope',
            methodology='Test investigation methodology',
            start_date='2023-01-01',
            estimated_completion='2023-03-31'
        )
        self.assertEqual(investigation.case, self.case)
        self.assertEqual(investigation.investigation_type, 'REGULATORY')
        self.assertEqual(investigation.scope, 'Test investigation scope')

    def test_ad_hoc_inspection_creation(self):
        """Test creating an ad-hoc inspection"""
        inspection = AdHocInspection.objects.create(
            case=self.case,
            trigger_type='COMPLAINT',
            inspection_scope='Test inspection scope',
            areas_of_focus='CDD, record-keeping',
            inspection_methodology='Test inspection methodology',
            estimated_duration=3
        )
        self.assertEqual(inspection.case, self.case)
        self.assertEqual(inspection.trigger_type, 'COMPLAINT')
        self.assertEqual(inspection.estimated_duration, 3)

    def test_case_attachment_creation(self):
        """Test creating a case attachment"""
        # Note: In a real test, you'd need to create a mock file
        attachment = CaseAttachment.objects.create(
            case=self.case,
            file_name='test_document.pdf',
            file_type='DOCUMENT',
            description='Test attachment description',
            uploaded_by=self.user
        )
        self.assertEqual(attachment.case, self.case)
        self.assertEqual(attachment.file_name, 'test_document.pdf')
        self.assertEqual(attachment.uploaded_by, self.user)

    def test_case_timeline_creation(self):
        """Test creating a case timeline event"""
        timeline_event = CaseTimeline.objects.create(
            case=self.case,
            event_type='CASE_OPENED',
            event_date='2023-01-01 10:00:00',
            description='Case opened for investigation',
            user=self.user
        )
        self.assertEqual(timeline_event.case, self.case)
        self.assertEqual(timeline_event.event_type, 'CASE_OPENED')
        self.assertEqual(timeline_event.user, self.user)

    def test_case_status_update(self):
        """Test updating case status"""
        old_status = self.case.status
        self.case.status = 'IN_PROGRESS'
        self.case.save()
        
        # Refresh from database
        self.case.refresh_from_db()
        self.assertEqual(self.case.status, 'IN_PROGRESS')
        self.assertNotEqual(self.case.status, old_status)

    def test_case_assignment(self):
        """Test assigning a case to a user"""
        new_user = User.objects.create_user(
            username='newuser',
            password='newpass123'
        )
        
        self.case.assigned_to = new_user
        self.case.save()
        
        # Refresh from database
        self.case.refresh_from_db()
        self.assertEqual(self.case.assigned_to, new_user)
        self.assertNotEqual(self.case.assigned_to, self.user)
