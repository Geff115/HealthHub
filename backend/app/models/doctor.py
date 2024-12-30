#!/usr/bin/env python3
"""
Doctor model
"""
from datetime import datetime
from .base import Base
from ..db.session import get_db_session
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import Session, relationship
from sqlalchemy import ForeignKey


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    doctor_username = Column(String, ForeignKey('users.username', ondelete='CASCADE'), unique=True, nullable=False)
    phone_number = Column(String(40), nullable=False)
    specialization = Column(String(80), nullable=False, index=True)
    license_number = Column(String(80), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Defining relationships between Doctor, User, Appointment, and Prescription
    user = relationship("User", back_populates='doctor')
    appointments = relationship("Appointment", back_populates='doctor', cascade="all, delete")
    prescriptions = relationship("Prescription", back_populates='doctor')
    medical_records = relationship("MedicalRecord", back_populates='doctor')


    def __repr__(self):
        """
        String representation of the Doctor
        """
        return f'<Doctor {self.id}>'
    
    @classmethod
    def get_doctor_by_id(cls, doctor_id):
        """
        Getting a doctor from the database based on the
        doctor id.
        """
        with get_db_session() as session:
            return session.query(cls).filter(cls.id == doctor_id).first()
    
    @classmethod
    def get_doctor_by_username(cls, doctor_username):
        """
        Getting a doctor from the database based on the
        doctor username
        """
        with get_db_session() as session:
            return session.query(cls).filter(cls.doctor_username == doctor_username).first()

    @classmethod
    def get_doctor_by_specialization(cls, specialization):
        """
        Getting a doctor from the database based on the
        doctor's specialization.
        """
        with get_db_session() as session:
            return session.query(cls).filter(cls.specialization == specialization).all()
