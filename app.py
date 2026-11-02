
import os
import sqlite3

from flask import Flask, jsonify, request
from auth import utilisateur_connecte

app = Flask(__name__)
DB = "notes.db"


def init_db():
    with sqlite3.connect(DB) as con:
        con.execute(
            "CREATE TABLE IF NOT EXISTS notes "
            "(id INTEGER PRIMARY KEY, etudiant TEXT, module TEXT, note REAL)"
        )
        if con.execute("SELECT COUNT(*) FROM notes").fetchone()[0] == 0:
            con.executemany(
                "INSERT INTO notes (etudiant, module, note) VALUES (?, ?, ?)",
                [
                    ("Amina", "DevSecOps", 15.5),
                    ("Youssef", "DevSecOps", 12.0),
                ],
            )


init_db()


@app.route("/")
def accueil():
    return (
        "<!DOCTYPE html><html lang='fr'><head><meta charset='utf-8'>"
        "<title>Notes des etudiants</title></head><body>"
        "<h1>Consultation des notes</h1>"
        "<p><a href='/notes'>Voir les notes</a></p></body></html>"
    )


@app.route("/health")
def health():
    return jsonify(status="ok")


@app.route("/notes")
def lister_notes():
    etudiant = request.args.get("etudiant", "")

    with sqlite3.connect(DB) as con:
        rows = con.execute(
            "SELECT id, etudiant, module, note FROM notes WHERE etudiant LIKE ?",
            (f"%{etudiant}%",),
        ).fetchall()

    return jsonify(
        [
            {"id": r[0], "etudiant": r[1], "module": r[2], "note": r[3]}
            for r in rows
        ]
    )


@app.route("/notes/<int:note_id>", methods=["PUT"])
def modifier_note(note_id):
    utilisateur = utilisateur_connecte()

    if utilisateur is None:
        return jsonify(erreur="Authentification requise"), 401

    if utilisateur.get("role") != "enseignant":
        return jsonify(erreur="Accès interdit"), 403

    donnees = request.get_json(silent=True) or {}
    nouvelle_note = donnees.get("note")

    if (
        isinstance(nouvelle_note, bool)
        or not isinstance(nouvelle_note, (int, float))
        or not 0 <= nouvelle_note <= 20
    ):
        return jsonify(erreur="Note invalide"), 400

    try:
        with sqlite3.connect(DB) as con:
            resultat = con.execute(
                "SELECT module FROM notes WHERE id = ?",
                (note_id,)
            ).fetchone()

            if resultat is None:
                return jsonify(erreur="Note introuvable"), 404

            module_note = resultat[0]

            if utilisateur.get("module") != module_note:
                return jsonify(erreur="Accès interdit"), 403

            con.execute(
                "UPDATE notes SET note = ? WHERE id = ?",
                (nouvelle_note, note_id)
            )

        return jsonify(status="ok"), 200

    except sqlite3.Error:
        return jsonify(erreur="Erreur interne"), 500


if __name__ == "__main__":
    app.run(host=os.environ.get("APP_HOST", "127.0.0.1"), port=5000)
