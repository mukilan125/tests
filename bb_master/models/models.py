# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResDistrict(models.Model):
    _name = "res.district"
    _description = "District"


    name = fields.Char('Name', required=True)    
    code = fields.Char('Code', required=True, size=4) 
    state_id = fields.Many2one("res.country.state", string='State', required=True)
    country_id = fields.Many2one("res.country", string='Country', required=True)
    
    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Code must be unique!'),
    ]

    @api.model
    @api.onchange('state_id')
    def onchange_on_state(self):
        self.country_id = self.state_id.country_id.id 


    @api.onchange('country_id')
    def onchange_country_id(self):
        """
        Onchange method of country to display states only in this country
        -----------------------------------------------------------------
        @param self : object pointer
        """
        res = {}
        dom = []
        if self.country_id:
            dom = [('country_id', '=', self.country_id.id)]
        res['domain'] = {
            'state_id':dom
        }
        return res


class ResCity(models.Model):
    _name = "res.city"
    _description = "Cities"

    name = fields.Char('Name', required=True)    
    code = fields.Char('Code', required=True, size=3) 
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict', required=True)
    country_id = fields.Many2one("res.country", string='Country', ondelete='restrict', required=True)
    district_id = fields.Many2one("res.district", string='District', ondelete='restrict', required=True)

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Code must be unique!'),
    ]

    @api.model
    @api.onchange('district_id')
    def onchange_on_district(self):
        self.state_id = self.district_id.state_id.id 

        res = {}
        dom = []
        if self.district_id:
            dom = [('district_id', '=', self.district_id.id)]
        res['domain'] = {
            'city_id':dom
        }
        return res

    @api.model
    @api.onchange('state_id')
    def onchange_on_state(self):
        self.country_id = self.state_id.country_id.id 
        res = {}
        dom = []
        if self.state_id:
            dom = [('state_id', '=', self.state_id.id)]
        res['domain'] = {
            'district_id':dom
        }
        return res 
        
    @api.onchange('country_id')
    def onchange_country_id(self):
        """
        Onchange method of country to display states only in this country
        -----------------------------------------------------------------
        @param self : object pointer
        """
        res = {}
        dom = []
        if self.country_id:
            dom = [('country_id', '=', self.country_id.id)]
        res['domain'] = {
            'state_id':dom
        }
        return res



class CollegeCampus(models.Model):
    _name = "college.campus"
    _description = "Campus"

    name = fields.Char('Campus Name', required=True)    
    code = fields.Char('Campus Code', required=True, size=6) 
    estd_date = fields.Date('Estd Date')

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Campus Code must be unique!'),
    ]

    _rec_name='code'    


class CollegeBlocks(models.Model):
    _name = "college.blocks"
    _description = "Blocks"


    name = fields.Char('Name', required=True)    
    code = fields.Char('Code', required=True) 
    campus_id = fields.Many2one("college.campus", string='Campus', ondelete='restrict', required=True)

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Block Code must be unique!'),
    ]



class CollegeBuilding(models.Model):
    _name = "college.building"
    _description = "Building"

    name = fields.Char('Building Name', required=True)    
    code = fields.Char('Building Code', required=True, size=3) 
    total_cost = fields.Integer('Total Cost')
    currency_id = fields.Many2one(string='Currency',comodel_name='res.currency')
    area = fields.Float("Area in Sq.m")
    
    campus_id = fields.Many2one("college.campus", string='Campus', ondelete='restrict', required=True)
    block_id = fields.Many2one("college.blocks", string='Block', ondelete='restrict', required=True)

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Building Code must be unique!'),
    ]


    @api.model
    @api.onchange('block_id')
    def onchange_on_blocks(self):
        self.campus_id = self.block_id.campus_id.id 
 
        
    @api.onchange('campus_id')
    def onchange_campus_id(self):
        """
        Onchange method of campus to display blocks only in this campus
        -----------------------------------------------------------------
        @param self : object pointer
        """
        res = {}
        dom = []
        if self.campus_id:
            dom = [('campus_id', '=', self.campus_id.id)]
        res['domain'] = {
            'block_id':dom
        }
        return res

class RoomLayout(models.Model):

    _name = 'room.layout'
    _description = "Room layout & maximum occupancy"

    # institution_id = fields.Many2one('college.campus', 'Institution', ondelete='restrict', required=True)
    institution_id = fields.Many2one('res.company', 'Institution', ondelete='restrict', required=True)
    
    name = fields.Char(
        string=u'Name', required=True
    ) 
    code = fields.Char(
        string=u'Code',required=True
    )
    row_count = fields.Integer('No of row\'s', required=True)
    column_count = fields.Integer('No of column\'s', required=True)  
    seat_per_col = fields.Integer('No of seats per column', required=True)
    total_seats = fields.Integer('Total no of seat\'s', readonly=True)

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Layout Code must be unique!'),
    ]

    @api.model
    @api.onchange('row_count', 'column_count', 'seat_per_col')
    def onchange_campus_id(self):
        """ 
        Onchange method to calculate total no of seats for each room layout 
        based on rows, column, seats in column
        --------------------------------------------------------------------
        @param self : object pointer
        """
        if(self.row_count & self.column_count & self.seat_per_col):
            # print('qwerty')
            self.total_seats = self.row_count * self.column_count * self.seat_per_col
            print(self.total_seats)
        # print("no funslkndijOKWEMFPOKWMFLMCIRMKVNAJKRKVNJNEAKVJNIEJAVLNNJVINI")


class RoomDetail(models.Model):
    _name='room.detail'
    _description = 'Create all rooms under buildings'
    
    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True)
    floor = fields.Char('Floor', required=True)
    building_id = fields.Many2one('college.building', 'Building', required=True)
    is_seminar = fields.Boolean('Is Seminar Hall')
    room_condition = fields.Selection([('available', 'Available'), ('maintenance', 'Maintenance')], "Type", default='available', required=True)
    room_layout_ids = fields.One2many('room.layout.line', 'room_id', 'Occupancies')
    
class RoomType(models.Model):
    _name = 'room.type'
    _description = "Room Type"

    name = fields.Char('Name')

class RoomLayoutLine(models.Model):
    _name = 'room.layout.line'
    _description = "Room layout line"

    layout_id = fields.Many2one('room.layout', 'Layout', required=True)
    room_type_id = fields.Many2one('room.type', 'Type')
    no_of_occupancy = fields.Integer('No of Occupancy')
    room_id = fields.Many2one('room.detail', 'Room')

# ***************************Academic Classes*************************
# --------------------------------------------------------------------

class AcademicYear(models.Model):
    _name = 'academic.year'
    _description = 'Transport vehicle details'

    institution_id = fields.Many2one("res.company", string='Institution', ondelete='restrict', required=True)
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    code = fields.Char('Educational Year Code')
    description = fields.Text('Description')
    semester_ids = fields.One2many('academic.semester', 'academic_year_id', 'Semester')

    _rec_name = 'code'

# Batch Semester tree
class AcademicSemester(models.Model):
    _name = 'academic.semester'
    _description = "Academic Semester"

    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    semester_no = fields.Char('Semester No')
    code = fields.Char('Code')
    name = fields.Char('Name')
    result_date = fields.Date('Due Date for Result update')
    academic_term = fields.Selection([("nonsemandsem", 'NonSem and Sem'), ('nonsem', 'NonSemester'), ('sem','Semester'), ('shortterm', 'Short Term Course'), ('trisem', 'Trisemester'), ('other', 'Other')], 'Academic Term')
    academic_year_id = fields.Many2one('academic.year', 'Academic Year')


class AcademicCourseType(models.Model):
    _name = 'academic.course.type'
    _description = "Academic Course type"

    code = fields.Char('Course Type')
    description = fields.Char('Description')
    category = fields.Selection([('certification', 'Certificate Course'), ('ug', 'Under Graduate'), ('pg', 'Post Graduate'), ('research', 'Research Scholar')], 'Course Category')
    degree_type = fields.Selection([('full', 'Full Time'), ('part', 'Part Time')], 'Degree Type')
    duration = fields.Integer('Duration')
    unit_id = fields.Selection([('years', 'Years'), ('months', 'Months'),
    ('weeks', 'Weeks'), ('days', 'Days'), ('hours', 'Hours'),
    ])

    _rec_name = 'code'

class AcademicCourse(models.Model):
    _name = 'academic.course'
    _description = "Academic Course"

    name = fields.Char('Course Name')
    institution_id = fields.Many2one("res.company", string='Institution', ondelete='restrict', required=True)
    course_type_id = fields.Many2one('academic.course.type', string='Course Type', ondelete='restrict', required=True)
    code = fields.Char('Course Code')

    _rec_name = 'name'

class Classes(models.Model):
    _name = 'academic.classes'
    _description = "Academic Classes"
    _rec_name = 'code'  

    institution_id = fields.Many2one("res.company", string='Institution', ondelete='restrict', required=True)
    name = fields.Char('Class Name')    
    code = fields.Char('Class Code')
    # Point it to staff master class later
    staff_dept = fields.Char('Staff Department')
    staff_name = fields.Char('Class Advisor')
    class_rep = fields.Char('Class Representative')
    rep_type = fields.Selection([
        ('placement', 'Placement'),('boys', 'Boys'), ('girls','Girls')
    ])
      

class AcademicBatch(models.Model):
    _name = 'academic.batch'
    _description = 'create all batch here for academic year'

    institution_id = fields.Many2one("res.company", string='Institution', ondelete='restrict', required=True)
    course_id = fields.Many2one('academic.course', string='Course', ondelete='restrict', required=True)
    from_academic_year_id = fields.Many2one('academic.year', 'From Academic Year')
    to_academic_year_id = fields.Many2one('academic.year', 'To Academic Year')
    name = fields.Char('Batch Name')
    regulation_id = fields.Char('Regulation')
    # regulation_id = fields.Many2one('academic.regulation', string='Regulation', ondelete='restrict', required=True)
    interview = fields.Boolean('Interview')
    is_active = fields.Boolean('Active')
    total_seat = fields.Integer('Total Seats')
    govn_seat = fields.Integer('Government Seats')
    mngt_seat = fields.Integer('Management Seats')
    govn_regular = fields.Integer('Government Regular Seats')
    govn_lateral = fields.Integer('Government Lateral Seats')
    mngt_regular = fields.Integer('Management Regular Seats')
    mngt_lateral = fields.Integer('Management Lateral Seats')
    filled_seat = fields.Integer('Filled Seats')
    entrance_date = fields.Date('Entrance Date')
    commencement_date = fields.Date('Date of Commencement')
    completion_date = fields.Date('Date of Completion')
    app_start_date = fields.Date('Application Start Date')
    app_end_date = fields.Date('Application End Date')
    online_app_end_date = fields.Date('Online Application End Date')
    roll_no_prefix = fields.Char('Roll No Prefix')
    suffix_length = fields.Char('Suffix Length')

    @api.onchange('institution_id')
    def onchange_for_coursename(self):
        """ Onchange for coursename """
        res = {}
        dom = []
        if self.institution_id: 
            dom = [('institution_id', '=', self.institution_id.id)]
        res['domain'] = { 'course_id':dom }
        return res

    _rec_name = 'name'

class AcademicRegulation(models.Model):

    _name = 'academic.regulation'
    _description = 'Create regulation for all batch'

    institution_id = fields.Many2one("res.company", string='Institution', ondelete='restrict', required=True)
    code = fields.Char('Name', required=True)
    desc = fields.Text('Description')
    from_date = fields.Date('Effective From')
    till_date = fields.Date('Effective Until')
    autonomous = fields.Boolean('Autonomous')
    follow_grade_sys = fields.Boolean('Follow Grade System')
    current_regulation = fields.Boolean('Active')
    program_ids = fields.One2many('academic.regulation.lines', 'regulation_id', 'Degree Programs')

    _rec_name = 'code'

class AcademicRegulationLines(models.Model):

    _name = 'academic.regulation.lines'
    _description = "Academic Regulation lines"

    regulation_id = fields.Many2one('academic.regulation', 'Regulation')
    program_id = fields.Many2one('academic.course', 'Degree Program', required='True')
    academic_term = fields.Selection([('semester', 'Semester'), ('nonsemester', 'Non Semester')], 'Academic Term')
    semester_count = fields.Selection([('one', '1'),('two', '2'), ('three', '3')], 'No of Semester')
    year_code = fields.Char('Year Code')