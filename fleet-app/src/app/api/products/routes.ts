import { sql } from '@vercel/postgres';
import { NextResponse } from 'next/server';

export async function GET(request: Request) {
const { searchParams } = new URL(request.url);
const name = searchParams.get('name');
const ownerName = searchParams.get('ownerName');

try {
    if (!name || !ownerName) throw new Error('name and owner names required');
    await sql`INSERT INTO NAME (name, Owner) VALUES (${name}, ${ownerName});`;
} catch (error) {
    return NextResponse.json({ error }, { status: 500 });
}

  const pets = await sql`SELECT * FROM Pets;`;
return NextResponse.json({ pets }, { status: 200 });
}